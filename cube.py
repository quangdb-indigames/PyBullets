import pybullet as p
import time
import pybullet_data
from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
import math
import random

class Cube():
	def __init__(self, pos, scale,  modelPath, cam, col_scale, col_local_pos = [0,0,0], isPlane = False):
		self.model = pyxie.figure(modelPath)
		self.model.position = pos
		self.model.scale = scale
		self.colBoxId = 0
		self.col_scale = col_scale
		self.col_local_pos = col_local_pos
		# Create box collider		
		self.isPlane = isPlane
		if not self.isPlane:
			self.createColBox(1)
			self.tapped = False
			self.cam = cam
			self.camDis = [0.0, -3.0, 3]
		else:
			self.createColBox(0)
	
	def update(self, touch):
		if self.isPlane:
			return
		self.autoRePosition()
		self.onClick(touch)
		

	def createColBox(self, mass):
		if self.model is None:
			return

		col_pos = [self.model.position.x + self.col_local_pos[0], self.model.position.y + self.col_local_pos[1], self.model.position.z + self.col_local_pos[2]]
		self.colBoxId = p.createCollisionShape(p.GEOM_BOX,
								  halfExtents=self.col_scale)
		boxId = p.createMultiBody(baseMass = mass, baseCollisionShapeIndex = self.colBoxId, basePosition= col_pos);
		p.changeDynamics(self.colBoxId, -1, linearDamping=5.0, lateralFriction=1, restitution=0.0)

	def onClick(self, touch):
		if touch:
			if touch['is_holded'] and not self.tapped:
				self.tapped = True
				pos, orn = p.getBasePositionAndOrientation(self.colBoxId)
				force = [0, -self.camDis[1] * 100, 500]
				p.applyExternalForce(self.colBoxId, -1, force, pos, flags = p.WORLD_FRAME)
			else:
				self.tapped = False
		else:
			self.tapped = False
	
	def autoRePosition(self):
		pos, orn = p.getBasePositionAndOrientation(self.colBoxId)
		model_pos = (pos[0] - self.col_local_pos[0], pos[1] - self.col_local_pos[1], pos[2] - self.col_local_pos[2] )
		self.model.position = vmath.vec3(model_pos)
		
		self.cam.position = self.model.position + vmath.vec3(self.camDis)
		self.cam.target = self.model.position

	def toWorldCoordinate(self, scrx, scry, worldz, cam):
		invproj = vmath.inverse(cam.projectionMatrix)
		invview = cam.viewInverseMatrix

		w,h = pyxie.viewSize()
		x = scrx / w * 2
		y = scry / h * 2

		pos = vmath.vec4(x, y,0.0, 1.0)
		npos = invproj * pos
		npos = invview * npos
		npos.z /= npos.w
		npos.x /= npos.w
		npos.y /= npos.w
		npos.w = 1.0
		pos = vmath.vec4(x, y,1.0, 1.0)
		fpos = invproj * pos
		fpos = invview * fpos
		fpos.z /= fpos.w
		fpos.x /= fpos.w
		fpos.y /= fpos.w
		fpos.w = 1.0

		dir = vmath.normalize(fpos - npos)
		print(npos + (dir * (npos.z - worldz)))
		return npos + (dir * (npos.z - worldz))