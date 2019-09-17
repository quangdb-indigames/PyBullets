class ClassManager:
	__instance = None
    
    @staticmethod 
	def getInstance():
		""" Static access method. """
		if ClassManager.__instance == None:
			ClassManager()
		return ClassManager.__instance
	def __init__(self):
		if ClassManager.__instance != None:
			raise Exception("This class is a singleton!")
		else:
			ClassManager.__instance = self