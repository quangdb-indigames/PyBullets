from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
import json
class SpeedButton():
	def __init__(self, pos, scale, tickScale, filePath, tickPath, showcase, moveSpeed):
		self.position = pos
		self.scale = scale
		self.tickScale = tickScale
		self.filePath = filePath
		self.tickPath = tickPath
		self.showcase = showcase
		self.moveSpeed = moveSpeed

		#Bar
		self.bar = graphicsHelper.createSprite(self.scale[0], self.scale[1], self.filePath)
		self.bar.position = vmath.vec3(self.position)
		self.showcase.add(self.bar)

		#Tick
		self.tickPosition = [self.position[0], self.position[1] - self.scale[1] / 2, self.position[2] + 1.0]
		self.tickModel = graphicsHelper.createSprite(self.tickScale[0], self.tickScale[1], self.tickPath)
		self.tickModel.position = vmath.vec3(self.tickPosition)
		self.showcase.add(self.tickModel)

		#Default stat
		self.normalZone = 1.0
		self.goodZone = 1.5
		self.perfectZone = 2.0

		self.disable = False
	
	def Update(self):
		if self.disable:
			return
		self.CheckChangeDirection()
		self.MoveTick()

	def CheckChangeDirection(self):
		if self.tickModel.position.y < self.position[1] - self.scale[1] / 2 + 10 and self.moveSpeed < 0:
			self.moveSpeed = -self.moveSpeed
		elif self.tickModel.position.y > self.position[1] + self.scale[1] / 2 - 10 and self.moveSpeed > 0: 
			self.moveSpeed = -self.moveSpeed
	
	def MoveTick(self):
		tickPos = [self.tickModel.position.x, self.tickModel.position.y + self.moveSpeed, self.tickModel.position.z]
		self.tickModel.position = vmath.vec3(tickPos)
	
	def GetCurrentTickZone(self):
		self.disable = True
		self.showcase.remove(self.bar)
		self.showcase.remove(self.tickModel)
		currentTick = self.tickModel.position.y - (self.position[1] - self.scale[1] / 2)

		#If currentTick 
		zone = currentTick / self.scale[1]

		if zone < 0.8:
			return self.normalZone
		elif zone < 0.95:
			return self.goodZone
		else:
			return self.perfectZone
	