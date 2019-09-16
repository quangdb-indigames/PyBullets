class Component():
	def __init__(self, gameObject):
		self.gameObject = gameObject
		self.listAttrToShow = []
	
	def update(self):
		pass

	def showOnInspector(self, attr):
		"""
		Make attr display on inspector
			----------
			Parameters
			----------
			attr: string
				name of attribute
			-------
			Returns
			-------
		"""
		self.listAttrToShow.append(attr)
		
	def removeSelf(self):
		del self.gameObject
		del self.listAttrToShow