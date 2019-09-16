import pyvmath as vmath
from modules.Helper.helperFunction import fromEulerToQuaternion
from modules.Object.transform import Transform
class GameObject():
	def __init__(self, name = "GameObject", position = [0.0,0.0,0.0], scale  = [1.0,1.0,1.0], rotation = [0.0,0.0,0.0]):
		# Parent - Child
		self.parent = None
		self.childs = []
		# Object name
		self.name = name

		self.transform = Transform(self, position, rotation, scale)

		# Object components
		self.components = []
		# self.components.append(self.transform)
	 
	def __repr__(self):
		return self.__class__.__name__
	
	def update(self, updateSelf = True):
		self.__autoTransformBaseParent(updateSelf)

		for component in self.components:
			try:
				component.update()
			except AttributeError:
				pass
		
		for gameObject in self.childs:
			try:
				gameObject.update()
			except AttributeError:
				pass

	def setParent(self, newParent):
		try:
			newParent.childs.append(self)
			self.parent = newParent

			localPosition, localRotation, localScale = newParent.transform.fromWorldToLocalTransform(self.transform)
			self.transform.localPosition = localPosition
			self.transform.localRotation = localRotation
			self.transform.localScale = localScale
		except AttributeError:
			print("New parent is not of type GameObject!!!")
	
	def removeParent(self):
		self.parent.childs.remove(self)
		self.parent = None

		# Local transform
		self.localPosition = self.position
		self.localScale = self.scale
		self.localRotation = self.rotation

	def getComponent(self, objType):
		for component in self.components:
			if isinstance(component, objType):
				return component
		return None
	
	def removeComponent(self, component):
		if isinstance(component, Transform):
			print("You can't remove transform of game object")
		else:
			component.removeSelf()
			self.components.remove(component)
	
	def __autoTransformBaseParent(self, updateSelf):
		if self.parent is None:
			return
		
		position, rotation, scale = self.parent.transform.fromLocalToWorldTransform(self.transform)
		self.transform.position = position
		self.transform.rotation = rotation
		self.transform.scale = scale
		

		


