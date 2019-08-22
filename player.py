import pybullet as p
import time
import pybullet_data
from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
import math
import random

class Player():
	def __init__(self, pos, scale, base_rotate, modelPath, cam, col_scale, col_local_pos = [0,0,0], camfollow = False):
		# Create model to display on pyxie
		self.model = pyxie.figure(modelPath)
		self.model.position = pos
		self.model.scale = scale
		self.base_rotate = base_rotate
		self.model.rotation = vmath.quat(self.base_rotate)
		# Create collider box to simulate physics on bullet physics
		self.colBoxId = 0
		self.col_scale = col_scale
		self.col_local_pos = col_local_pos

		# Create box collider		
		self.camFollow = camfollow

		self.__createColBox(1)
		self.tapped = False

		# Should this player have camera follow behind?
		if self.camFollow:
			self.cam = cam
			self.camDis = [0.0, -3.0, 3]
	
	def update(self, touch):
		self.__autoRePosition()
		if not self.camFollow:
			return
		self.__onClick(touch)
		

	def __createColBox(self, mass):
		col_pos = [self.model.position.x + self.col_local_pos[0], self.model.position.y + self.col_local_pos[1], self.model.position.z + self.col_local_pos[2]]
		self.colBoxId = p.createCollisionShape(p.GEOM_BOX,
								  halfExtents=self.col_scale)
		boxId = p.createMultiBody(baseMass = mass, baseCollisionShapeIndex = self.colBoxId, basePosition= col_pos);
		p.changeDynamics(self.colBoxId, -1, linearDamping=5.0, lateralFriction=1, restitution=0.4)

	def __onClick(self, touch):
		if touch:
			if touch['is_holded'] and not self.tapped:
				self.tapped = True
				self.__onClickExcute()
			else:
				self.tapped = False
		else:
			self.tapped = False
	
	def __autoRePosition(self):
		pos, orn = p.getBasePositionAndOrientation(self.colBoxId)
		
		# print("Col pos is: ", pos)
		# print("Model pos is: ", self.model.position)
		quat = self.__autoReRotation(orn)
		self.model.rotation = quat		
		# quat_normalized = vmath.normalize(vmath.quat(orn))
		local_v = vmath.rotate(vmath.vec3(self.col_local_pos), vmath.quat(orn))
		pos_x = pos[0] - local_v.x
		pos_y = pos[1] - local_v.y
		pos_z = pos[2] - local_v.z
		model_pos = (pos_x, pos_y, pos_z)
		self.model.position = vmath.vec3(model_pos)
		if self.camFollow:
			self.cam.position = self.model.position + vmath.vec3(self.camDis)
			self.cam.target = self.model.position + vmath.vec3(0, 0, 0)
	
	def __onClickExcute(self):
		pos, orn = p.getBasePositionAndOrientation(self.colBoxId)
		force = [0, -self.camDis[1] * 500, 300]
		p.applyExternalForce(self.colBoxId, -1, force, pos, flags = p.WORLD_FRAME)

	def __autoReRotation(self, rot_quat):
		fin_quat = vmath.mul(vmath.quat(rot_quat), vmath.quat(self.base_rotate))
		return fin_quat

	def onContact(self):
		aabbMin, aabbMax = p.getAABB(self.colBoxId, -1)
		collision_list = p.getOverlappingObjects(aabbMin, aabbMax)