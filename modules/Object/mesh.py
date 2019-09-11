from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
from modules.Object.component import Component
from modules.Helper import helperFunction
class Mesh(Component):
	def __init__(self, gameObject, meshData):
		super().__init__(gameObject)
		self.mesh = pyxie.figure(meshData)
		self.mesh.position = vmath.vec3(self.gameObject.position)
		self.mesh.rotation = vmath.quat(helperFunction.fromEulerToQuaternion(self.gameObject.rotation))
		self.mesh.scale = vmath.vec3(self.gameObject.scale)
	
	def update(self):
		super().update()
		self.__autoReTransform()
	
	def __autoReTransform(self):
		self.mesh.position = vmath.vec3(self.gameObject.position)
		self.mesh.rotation = vmath.quat(helperFunction.fromEulerToQuaternion(self.gameObject.rotation))
		self.mesh.scale = vmath.vec3(self.gameObject.scale)
	
	def replaceMesh(self, meshData):
		self.mesh = pyxie.figure(meshData)
		self.mesh.position = vmath.vec3(self.gameObject.position)
		self.mesh.rotation = vmath.quat(helperFunction.fromEulerToQuaternion(self.gameObject.rotation))
		self.mesh.scale = vmath.vec3(self.gameObject.scale)