import pybullet as p
import time
import pybullet_data
from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
import math
import random

class Player():
	def __init__(self, pos, scale,  modelPath, cam, col_scale, col_local_pos = [0,0,0], camfollow = False):
		# Create model to display on pyxie
		self.model = pyxie.figure(modelPath)
		self.model.position = pos
		self.model.scale = scale

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
		p.changeDynamics(self.colBoxId, -1, linearDamping=5.0, lateralFriction=1, restitution=0.0)

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
		model_pos = (pos[0] - self.col_local_pos[0], pos[1] - self.col_local_pos[1], pos[2] - self.col_local_pos[2] )
		self.model.position = vmath.vec3(model_pos)
		if self.camFollow:
			self.cam.position = self.model.position + vmath.vec3(self.camDis)
			self.cam.target = self.model.position
	
	def __onClickExcute(self):
		pos, orn = p.getBasePositionAndOrientation(self.colBoxId)
		force = [0, -self.camDis[1] * 500, 1000]
		p.applyExternalForce(self.colBoxId, -1, force, pos, flags = p.WORLD_FRAME)