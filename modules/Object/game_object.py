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

		# Type display transform
		self.displayTransform = [self.position, self.rotation, self.scale]

		# Object components
		self.components = []
	 
	def __repr__(self):
		print("Class: ", self.__class__, ", Object's name: ", self.name)
	
	def update(self):
		self.__autoTransformBaseParent()

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

			localPos = [newParent.position[0] - self.position[0], newParent.position[1] - self.position[1], newParent.position[2] - self.position[2]]
			localRotation = [newParent.rotation[0] - self.rotation[0], newParent.rotation[1] - self.rotation[1], newParent.rotation[2] - self.rotation[2]]
			localScale = [newParent.rotation[0] / self.rotation[0], newParent.rotation[1] / self.rotation[1], newParent.rotation[2] / self.rotation[2]]

			self.localPosition = localPos
			self.localRotation = localRotation
			self.localScale = localScale

			self.displayTransform = [self.localPosition, self.localRotation, self.localScale]
		except AttributeError:
			print("New parent is not of type GameObject!!!")
	
	def removeParent(self):
    	self.parent.childs.remove(self)
		self.parent = None

		# Local transform
		self.localPosition = None
		self.localScale = None
		self.localRotation = None

		# Type display transform
		self.displayTransform = [self.position, self.rotation, self.scale]

	
	def __autoTransformBaseParent(self):
		if self.parent is None:
			return
		
		self.position = [self.parent.position[0] + self.localPosition[0], self.parent.position[1] + self.localPosition[1], self.parent.position[2] + self.localPosition[2]]
		self.rotation = [self.parent.rotation[0] + self.localRotation[0], self.parent.rotation[1] + self.localRotation[1], self.parent.rotation[2] + self.localRotation[2]]
		self.scale = [self.parent.scale[0] * self.localScale[0], self.parent.scale[1] * self.localScale[1], self.parent.scale[2] * self.localScale[2]]

		


