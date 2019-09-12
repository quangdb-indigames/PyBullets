import pyvmath as vmath
from modules.Helper.helperFunction import fromEulerToQuaternion
class GameObject():
	def __init__(self, name = "GameObject", position = [0,0,0], scale  = [1,1,1], rotation = [0,0,0]):
		# Parent - Child
		self.parent = None
		self.childs = []
		# Object name
		self.name = name

		# Global transform
		self.position = position
		self.scale = scale
		self.rotation = rotation
		
		# Local transform
		self.localPosition = None
		self.localScale = None
		self.localRotation = None

		# Object components
		self.components = []
	 
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

			localPos = [self.position[0] - newParent.position[0], self.position[1] - newParent.position[1], self.position[2] - newParent.position[2]]
			localRotation = [self.rotation[0] - newParent.rotation[0], self.rotation[1] - newParent.rotation[1], self.rotation[2] - newParent.rotation[2]]
			localScale = [self.scale[0] / newParent.scale[0], self.scale[1] / newParent.scale[1], self.scale[2] / newParent.scale[2]]

			self.localPosition = localPos
			self.localRotation = localRotation
			self.localScale = localScale

		except AttributeError:
			print("New parent is not of type GameObject!!!")
	
	def removeParent(self):
		self.parent.childs.remove(self)
		self.parent = None

		# Local transform
		self.localPosition = None
		self.localScale = None
		self.localRotation = None

	def getComponent(self, objType):
		for component in self.components:
			if isinstance(component, objType):
				return component
		return None
	
	def __autoTransformBaseParent(self, updateSelf):
		if self.parent is None:
			return
		
		# Current dont use child because this is not correct

		if updateSelf:
			rot = [self.parent.rotation[0] - self.localRotation[0], self.parent.rotation[1] - self.localRotation[1], self.parent.rotation[2] - self.localRotation[2]]
			quat = fromEulerToQuaternion(rot)
			curLocalPos = vmath.vec3(self.localPosition)
			newLocalPos = vmath.rotate(curLocalPos, vmath.quat(quat))		
			self.position = [self.parent.position[0] + newLocalPos.x, self.parent.position[1] + newLocalPos.y, self.parent.position[2] + newLocalPos.z]
		else:
			self.position = [self.parent.position[0] + self.localPosition[0], self.parent.position[1] + self.localPosition[1], self.parent.position[2] + self.localPosition[2]]
		self.rotation = [self.parent.rotation[0] + self.localRotation[0], self.parent.rotation[1] + self.localRotation[1], self.parent.rotation[2] + self.localRotation[2]]
		self.scale = [self.parent.scale[0] * self.localScale[0], self.parent.scale[1] * self.localScale[1], self.parent.scale[2] * self.localScale[2]]

		


