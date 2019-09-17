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
		self.transform.update()
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
	
	def destroy(self):
		for component in self.components:
			component.removeSelf()
		del self.components

		for child in self.childs:
			child.destroy()
		del self.childs
		del self.transform
		del self.parent
		del self.name
