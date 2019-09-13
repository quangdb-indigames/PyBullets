from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
from modules.Object.collider import Collider
from modules.Helper import helperFunction
class BoxCollider(Collider):
	def __init__(self, gameObject, colliderPath, showcase):
		super().__init__(gameObject)
		self.colType = "BOX COLLIDER"
		self.showOnInspector("colType")

		self.scale = self.gameObject.scale		
		self.showOnInspector("scale")
		self.isDisplay = True
		self.showOnInspector("isDisplay")
		self.showcase = showcase

		self.mesh = pyxie.figure(colliderPath)
		self.mesh.position = vmath.vec3(self.gameObject.position)
		self.mesh.rotation = vmath.quat(helperFunction.fromEulerToQuaternion(self.gameObject.rotation))
		self.mesh.scale = vmath.vec3(self.gameObject.scale)
		self.showcase.add(self.mesh)
	
	def update(self):
		super().update()
		self.__checkDisplay()
		self.__autoReTransform()

	def __checkDisplay(self):
		try:
			self.showcase.remove(self.mesh)
		except:
			pass
			
		if self.isDisplay:
			self.showcase.add(self.mesh)
	
	def __autoReTransform(self):
		self.mesh.position = vmath.vec3(self.gameObject.position)
		self.mesh.rotation = vmath.quat(helperFunction.fromEulerToQuaternion(self.gameObject.rotation))
		self.mesh.scale = vmath.vec3(self.scale)