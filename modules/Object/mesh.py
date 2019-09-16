from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
from modules.Object.component import Component
from modules.Helper import helperFunction
from modules.Scene.SceneManager import SceneManager
class Mesh(Component):
	def __init__(self, gameObject, meshData):
		super().__init__(gameObject)
		self.meshName = meshData
		self.showOnInspector("meshName")

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
	
	def removeSelf(self):
		super().removeSelf()
		currentScene = SceneManager.Singleton_GetCurrentScene()
		currentScene.showcase.remove(self.mesh)
		del self.meshName
		del self.mesh
		