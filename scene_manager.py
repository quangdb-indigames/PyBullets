class SceneManager:
	"""
	This should be manage all scene
	"""
	__instance = None
	__currentScene = None

	@staticmethod 
	def getInstance():
		""" Static access method. """
		if SceneManager.__instance == None:
			SceneManager()
		return SceneManager.__instance
	def __init__(self):
		if SceneManager.__instance != None:
			raise Exception("This class is a singleton!")
		else:
			SceneManager.__instance = self
	
	@staticmethod
	def GetCurrentScene():
		"""
		Return current scene
		"""
		return SceneManager.__currentScene

	@staticmethod
	def SetCurrentScene(scene):
		SceneManager.__currentScene = scene