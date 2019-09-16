from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
from modules.Object.component import Component
from modules.Helper import helperFunction
class Mesh(Component):
	def __init__(self, gameObject, meshData):
		super().__init__(gameObject)
		self.meshName = meshData
		self.showOnInspector("meshName")
		self.testAttr = [5.89, 81.19, 12.12, 89.12, 99.12]
		self.showOnInspector("testAttr")

		self.mesh = pyxie.figure(meshData)
		self.mesh.position = vmath.vec3(self.gameObject.transform.position)
		self.mesh.rotation = vmath.quat(helperFunction.fromEulerToQuaternion(self.gameObject.transform.rotation))
		self.mesh.scale = vmath.vec3(self.gameObject.transform.scale)
	
	def update(self):
		super().update()
		self.__autoReTransform()
	
	def __autoReTransform(self):
		self.mesh.position = vmath.vec3(self.gameObject.transform.position)
		self.mesh.rotation = vmath.quat(helperFunction.fromEulerToQuaternion(self.gameObject.transform.rotation))
		self.mesh.scale = vmath.vec3(self.gameObject.transform.scale)
	
	def replaceMesh(self, meshData):
		self.meshName = meshData
		self.mesh = pyxie.figure(meshData)
		self.mesh.position = vmath.vec3(self.gameObject.transform.position)
		self.mesh.rotation = vmath.quat(helperFunction.fromEulerToQuaternion(self.gameObject.transform.rotation))
		self.mesh.scale = vmath.vec3(self.gameObject.transform.scale)