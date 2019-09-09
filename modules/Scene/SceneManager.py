class SceneManager:
	__instance = None
	currentScene = 0
	previousScene = -1
	list_scene = []

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
	def Singleton_GetCurrentScene():
		return SceneManager.list_scene[SceneManager.currentScene]
	
	@staticmethod
	def Singleton_GetPreviousScene():
		if SceneManager.previousScene == -1:
			return None
		return SceneManager.list_scene[SceneManager.previousScene]

	@staticmethod
	def Singleton_NextScene():
		SceneManager.previousScene = SceneManager.currentScene
		SceneManager.currentScene += 1
		if SceneManager.currentScene > len(SceneManager.list_scene) - 1:
			SceneManager.currentScene = len(SceneManager.list_scene) - 1
		
		return SceneManager.list_scene[SceneManager.currentScene].__init__()
	
	@staticmethod
	def Singleton_PreviousScene():
		SceneManager.previousScene = SceneManager.currentScene
		SceneManager.currentScene -= 1
		if SceneManager.currentScene < 0:
			SceneManager.currentScene = 0
		
		return SceneManager.list_scene[SceneManager.currentScene].__init__()