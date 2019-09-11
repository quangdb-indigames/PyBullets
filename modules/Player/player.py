from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
import math
from modules.Helper import helperFunction
class Player():
	def __init__(self, position, scale, rotation, modelPath, showcase, cam):
		self.position = position
		self.scale = scale
		self.rotation = rotation
		self.modelPath = modelPath
		self.cam = cam
		self.showcase = showcase
		
		# Setting up
		self.model = pyxie.figure(modelPath)
		self.model.position = vmath.vec3(self.position)
		self.model.scale = vmath.vec3(self.scale)
		self.model.rotation = vmath.quat(helperFunction.fromEulerToQuaternion(self.rotation))
		self.showcase.add(self.model)
	
	def update(self):
		self.model.position = vmath.vec3(self.position)
		self.model.scale = vmath.vec3(self.scale)
		self.model.rotation = vmath.quat(helperFunction.fromEulerToQuaternion(self.rotation))