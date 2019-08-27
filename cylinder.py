import pybullet as p
import time
import pybullet_data
from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
import math
import random

class Cylinder():
	def __init__(self, pos, scale,  modelPath, col_radius, col_height, col_local_pos = [0,0,0], base_quaternion = [0, 0, 0, 1], isStatic = False, isIteractable = False):
		# Create model to display on pyxie
		self.model = pyxie.figure(modelPath)
		self.model.position = pos
		self.model.scale = scale
		self.base_rotate = base_quaternion
		self.model.rotation = vmath.quat(self.base_rotate)

		# Create collider to simulate physics on bullet physics
		self.colId = 0
		self.col_radius = col_radius
		self.col_height = col_height
		self.col_local_pos = col_local_pos

		# Create box collider		
		self.isIteractable = isIteractable
		self.isStatic = isStatic
		if self.isStatic:
			self.__createCollider(0)
		else:
			self.__createCollider(1)

		# Depend on cube type should be iteractable or not
		if self.isIteractable:
			self.tapped = False
	
	def update(self, touch):
		if not self.isStatic:
			self.__autoRePosition()

		if not self.isIteractable:
			return
		self.__onClick(touch)
		

	def __createCollider(self, mass):
		if self.model is None:
			return

		col_pos = [self.model.position.x + self.col_local_pos[0], self.model.position.y + self.col_local_pos[1], self.model.position.z + self.col_local_pos[2]]
		self.colId = p.createCollisionShape(p.GEOM_CYLINDER,
								  radius = self.col_radius, height = self.col_height)
		boxId = p.createMultiBody(baseMass = mass, baseCollisionShapeIndex = self.colId, basePosition= col_pos);
		p.changeDynamics(self.colId, -1, linearDamping=5.0, lateralFriction=1, restitution=0.0)

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
		pos, orn = p.getBasePositionAndOrientation(self.colId)
		quat = self.__autoReRotation(orn)
		self.model.rotation = quat
		local_v = vmath.rotate(vmath.vec3(self.col_local_pos), vmath.quat(orn))
		pos_x = pos[0] - local_v.x
		pos_y = pos[1] - local_v.y
		pos_z = pos[2] - local_v.z
		model_pos = (pos_x, pos_y, pos_z)
		self.model.position = vmath.vec3(model_pos)
	
	def __autoReRotation(self, rot_quat):
		fin_quat = vmath.mul(vmath.quat(rot_quat), vmath.quat(self.base_rotate))
		return fin_quat

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

	def __onClickExcute(self):
		pass
	
	def __autoReRotation(self, rot_quat):
		fin_quat = vmath.mul(vmath.quat(rot_quat), vmath.quat(self.base_rotate))
		return fin_quat