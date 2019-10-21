import pybullet as p
import time
import pybullet_data
from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
import math
import random
STATUS_STAY = 0
STATUS_WALK = 1
STATUS_RUN = 2
STATE_MOTION = {STATUS_STAY:"Sapphiart@idle", STATUS_WALK:"Sapphiart@walk", STATUS_RUN:"Sapphiart@running"}

class Player():
	def __init__(self, pos, scale, base_rotate, modelPath, cam, col_scale, col_local_pos = [0,0,0], camfollow = False):
		# Create model to display on pyxie
		self.model = pyxie.figure(modelPath)
		self.model.position = pos
		self.model.scale = scale
		self.base_rotate = base_rotate
		self.model.rotation = vmath.quat(self.base_rotate)
		# self.currentState = STATUS_STAY
		# self.model.connectAnimator(pyxie.ANIMETION_SLOT_A0, STATE_MOTION[self.currentState])
		# Create collider box to simulate physics on bullet physics
		self.colId = 0
		self.col_scale = col_scale
		self.col_local_pos = col_local_pos
		self.lastContactId = -1
		self.firstClick = False

		# Create box collider		
		self.camFollow = camfollow

		self.__createColBox(10)
		self.tapped = False
		self.dragged = False
		
		# Should this player have camera follow behind?
		if self.camFollow:
			self.cam = cam
			self.camDis = [0.0, -2.0, 3]
		print("Created")
	
	def update(self, touch, obj_list):
		self.__autoRePosition()
		# self.model.step()
		if not self.camFollow:
			return
		self.__onClick(touch)
		
		self.checkContact(obj_list)


	def __createColBox(self, mass):
		col_pos = [self.model.position.x + self.col_local_pos[0], self.model.position.y + self.col_local_pos[1], self.model.position.z + self.col_local_pos[2]]
		self.colId = p.createCollisionShape(p.GEOM_CAPSULE, radius=0.3)
		boxId = p.createMultiBody(baseMass = mass, baseCollisionShapeIndex = self.colId, basePosition= col_pos);
		p.changeDynamics(self.colId, -1, linearDamping=500.0, lateralFriction=0.1, restitution=0.4)

	def __onClick(self, touch):
		if touch:
			if touch['is_holded'] and not self.tapped and not self.firstClick:
				print("Tapped")
				self.tapped = True
				self.__onClickExcute()
			elif touch['is_holded'] and self.firstClick and not self.dragged:
				self.__onDragExcute(touch)
			else:
				self.tapped = False
		else:
			self.tapped = False
			self.dragged = False
	
	def __autoRePosition(self):
		pos, orn = p.getBasePositionAndOrientation(self.colId)
		quat = self.__autoReRotation(orn)
		self.model.rotation = quat		
		local_v = vmath.rotate(vmath.vec3(self.col_local_pos), vmath.quat(orn))
		pos_x = pos[0] - local_v.x
		pos_y = pos[1] - local_v.y
		pos_z = pos[2] - local_v.z
		model_pos = (pos_x, pos_y, pos_z)
		self.model.position = vmath.vec3(model_pos)

		# If this character have camfollow, make camera follow it
		if self.camFollow:
			self.cam.position = vmath.vec3(pos) + vmath.vec3(self.camDis)
			self.cam.target = vmath.vec3(pos)
	
	def __onClickExcute(self):
		if not self.firstClick:
			self.firstClick = True
			pos, orn = p.getBasePositionAndOrientation(self.colId)
			force = [0, -self.camDis[1] * 10000 * 2, 20000 * 1.2]
			p.applyExternalForce(self.colId, -1, force, pos, flags = p.WORLD_FRAME)
	
	def __onDragExcute(self, touch):
		direction = touch['cur_x'] - touch['org_x']
		if abs(direction) < 1:
			return
		if direction < 0:
			force = [-5000, 0, 0]
		else:
			force = [5000, 0, 0]
		pos, orn = p.getBasePositionAndOrientation(self.colId)
		p.applyExternalForce(self.colId, -1, force, pos, flags = p.WORLD_FRAME)
		self.dragged = True

	def __autoReRotation(self, rot_quat):
		fin_quat = vmath.mul(vmath.quat(rot_quat), vmath.quat(self.base_rotate))
		return fin_quat

	def checkContact(self, obj_list):
		aabbMin, aabbMax = p.getAABB(self.colId, -1)
		collision_list = p.getOverlappingObjects(aabbMin, aabbMax)
		if collision_list is not None and len(collision_list) != 0:		
			for objId in collision_list:
				obj = obj_list.get(str(objId[0]))
				if objId[0] != self.colId and objId[0] != self.lastContactId and obj is not None:
					self.lastContactId = objId[0]
					print("Have a contact")
					self.onContact(obj)
	
	def onContact(self, obj):
		print("Contact with ", obj.colId)
		pos, orn = p.getBasePositionAndOrientation(self.colId)
		force = [0, -self.camDis[1] * 2000, 8000]
		p.applyExternalForce(self.colId, -1, force, pos, flags = p.WORLD_FRAME)