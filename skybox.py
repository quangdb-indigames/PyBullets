import pyxie
import pyvmath as vmath
class Skybox:
	def __init__(self, skyboxPath, gameCamera, skyboxCamera, skyboxShowcase):
		self.skyboxPath = skyboxPath
		self.skybox = pyxie.figure(self.skyboxPath)
		self.skybox.scale = vmath.vec3([900.0, 900.0, 900.0])
		self.skybox.position = vmath.vec3([0.0, 0.0, -1000.0])
		# self.skybox.rotation = vmath.quat([ 0.7071068, 0, 0, 0.7071068 ])
		self.skyboxShowcase = skyboxShowcase
		self.skyboxShowcase.add(self.skybox)

		self.gameCamera = gameCamera
		self.skyboxCamera = skyboxCamera
	
	def Update(self):
		self.SyncCameraRotate()

	def SyncCameraRotate(self):
		self.skyboxCamera.rotation = self.gameCamera.rotation