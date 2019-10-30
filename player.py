import pybullet as p
import time
import pybullet_data
from pyxie.apputil import graphicsHelper
import pyxie
from scene_manager import SceneManager
import pyvmath as vmath
import math
import random
import json
STATUS_STAY = 0
STATUS_FLY = 1
STATE_MOTION = {STATUS_FLY:"betakkuma@fly02"}
TRANSIT_TIME = 0.2
MOVING_DISTANCE = 0.5

PLAYER_STATUS_DEATH = "PLAYER_STATUS_DEATH"

class Player():
	def __init__(self, pos, scale, base_rotate, modelPath, cam, col_scale, col_local_pos = [0,0,0], camfollow = False):
		# Create model to display on pyxie
		self.model = pyxie.figure(modelPath)
		self.model.position = pos
		self.model.scale = scale
		self.base_rotate = base_rotate
		self.model.rotation = vmath.quat(self.base_rotate)
		self.currentState = STATUS_STAY
		self.nextState = STATUS_STAY
		# self.model.connectAnimator(pyxie.ANIMETION_SLOT_A0, STATE_MOTION[self.currentState])
		# Create collider box to simulate physics on bullet physics
		self.colId = 0
		self.col_scale = col_scale
		self.col_local_pos = col_local_pos
		self.lastContactId = -1
		self.firstClick = False
		self.transitTime = 0.0

		# Create box collider		
		self.camFollow = camfollow

		self.__createColBox(10)
		self.tapped = False
		self.dragged = False
		self.abortCheckContact = False
		self.kEpsilon = 1.0
		self.isDeath = False
		
		# Should this player have camera follow behind?
		if self.camFollow:
			self.cam = cam
			self.camDis = [0.0, -3.0, 2.0]
		
		# Previous touch
		self.previousTouchX = 0
	
	def update(self, dt, touch, obj_list, ui_manager=None):
		self.__TransitMotion(dt)	
		self.model.step()

		# if self.firstClick and not self.isDeath:
		# 	self.CheckDeath()
		if self.isDeath:
			self.MoveCameraOnDeath()
			return

		self.__autoRePosition()

		if not ui_manager or ui_manager.isTouchOnUI == False:
			self.__onClick(touch)
		
		if not self.abortCheckContact:
			self.checkContact(obj_list)

		if not self.camFollow:
			return
		self.CameraFollow()

	def MoveCameraOnDeath(self):
		pass
		

	def __createColBox(self, mass):
		col_pos = [self.model.position.x + self.col_local_pos[0], self.model.position.y + self.col_local_pos[1], self.model.position.z + self.col_local_pos[2]]
		self.colId = p.createCollisionShape(p.GEOM_CAPSULE, radius=0.3)
		# start euler = (-45, 0, 0)
		self.colId = p.createMultiBody(baseMass = 0, baseCollisionShapeIndex = self.colId, basePosition= col_pos, baseOrientation=[ 0.4871745, 0, 0, -0.8733046 ]);
		p.changeDynamics(self.colId, -1, linearDamping=500.0, lateralFriction=0.1, restitution=0)

	def __onClick(self, touch):
		if touch:
			if touch['is_holded'] and not self.tapped and not self.firstClick:
				self.tapped = True
				self.__onClickExcute()
			elif touch['delta_x'] != 0 and self.firstClick:
				# if self.model.position.z > 0.5:
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
	
	def CameraFollow(self):
		# If this character have camfollow, make camera follow it
		if self.camFollow:
			self.cam.position = self.model.position + vmath.vec3(self.camDis)
			self.cam.target = self.model.position
	
	def __onClickExcute(self):
		if not self.firstClick:
			p.changeDynamics(self.colId, -1, 10)
			self.base_rotate = [0,0,1,0]
			self.col_local_pos = [0,0,0]
			self.__ChangeStatus(STATUS_FLY)	
			currentScene = SceneManager.GetCurrentScene()
			multi = currentScene.speedButton.GetCurrentTickZone()
			currentScene.SetState("STATE_PLAYING")
			currentScene.pauseButton.Display()
			self.firstClick = True
			data = self.GetData()
			if data:
				farMul, highMul = data['baseFarMultiply'], data['baseHighMultiply']
			else:
				farMul, highMul = 1.0, 1.0
			farMul = farMul * multi
			highMul = highMul * 0.5 * multi
			pos, orn = p.getBasePositionAndOrientation(self.colId)
			force = [0, -self.camDis[1] * 10000 * farMul, 20000 * highMul]
			p.applyExternalForce(self.colId, -1, force, pos, flags = p.WORLD_FRAME)
		
	def GetData(self):
		data = None
		try:
			with open("data/player/data.json", "r") as f:
				data = json.load(f)
		except:
			print("File not exist")
		return data
	
	def __onDragExcute(self, touch):
		direction = touch['delta_x']
		if direction < 0:
			force = [-2000, 0, 0]
		else:
			force = [2000, 0, 0]
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
					self.onContact(obj)
	
	def onContact(self, obj):
		p.resetBaseVelocity(self.colId, [0,0,0])
		pos, orn = p.getBasePositionAndOrientation(self.colId)
		newPos = [pos[0], pos[1] + 0.5, pos[2]]
		p.resetBasePositionAndOrientation(self.colId, newPos, orn)
		force = [0, -self.camDis[1] * 15000, 10000]
		p.applyExternalForce(self.colId, -1, force, newPos, flags = p.WORLD_FRAME)

	def __ChangeStatus(self, status):
		if status != self.currentState and status != self.nextState:
			self.nextState = status
			self.model.connectAnimator(pyxie.ANIMETION_SLOT_A1, STATE_MOTION[status])
			self.transitTime = 0.0
	
	def __TransitMotion(self, dt):
		if self.currentState != self.nextState:
			if self.transitTime >= TRANSIT_TIME:
				self.currentState = self.nextState
				self.model.connectAnimator(pyxie.ANIMETION_SLOT_A0, STATE_MOTION[self.currentState])
				self.model.connectAnimator(pyxie.ANIMETION_SLOT_A1)
				return

			self.transitTime += dt
			if self.transitTime > TRANSIT_TIME:
				self.transitTime = TRANSIT_TIME
			self.model.setBlendingWeight(pyxie.ANIMETION_PART_A, self.transitTime / TRANSIT_TIME)
	
	def CheckDeath(self):
		linearVelocity, angularVelocity = p.getBaseVelocity(self.colId)
		velocity = vmath.length(vmath.vec3(linearVelocity))
		if velocity < self.kEpsilon:
			self.isDeath = True
			# p.changeDynamics(self.colId, -1, mass=0)