from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
from scene_manager import SceneManager
class DestroyBar():
	def __init__(self, pos, backgroundBarScale, sliderBarScale, tickScale, backgroundBarPath, sliderBarPath, tickPath, showcase):
		# Supporting attribute
		self.percentComplete = 0.95
		self.onAlert = False
		self.oneStarPercent = 0.5
		self.twoStarPercent = 0.6
		self.threeStarPercent = 0.8
		self.isDisable = True
		
		# Background bar
		self.backgroundBarPos = pos
		self.backgroundBarScale = backgroundBarScale
		self.backgroundBarPath = backgroundBarPath
		self.backgroundBar = graphicsHelper.createSprite(self.backgroundBarScale[0], self.backgroundBarScale[1], self.backgroundBarPath)
		self.backgroundBar.position = vmath.vec3(self.backgroundBarPos)

		# Slider bar
		self.sliderBarPos = [self.backgroundBarPos[0] - self.backgroundBarScale[0] / 2 + (sliderBarScale[0] * self.percentComplete) / 2, self.backgroundBarPos[1], self.backgroundBarPos[2] + 1.0]
		self.sliderBarScale = sliderBarScale
		self.sliderBarPath = sliderBarPath
		self.sliderBar = graphicsHelper.createSprite(self.sliderBarScale[0], self.sliderBarScale[1], self.sliderBarPath)
		self.sliderBar.position = vmath.vec3(self.sliderBarPos)

		# Tick
		self.oneStarTickPos = [self.backgroundBarPos[0] - self.backgroundBarScale[0] / 2 + self.backgroundBarScale[0] * self.oneStarPercent, self.backgroundBarPos[1], self.backgroundBarPos[2] + 2.0]
		self.twoStarTickPos = [self.backgroundBarPos[0] - self.backgroundBarScale[0] / 2 + self.backgroundBarScale[0] * self.twoStarPercent, self.backgroundBarPos[1], self.backgroundBarPos[2] + 2.0]
		self.threeStarTickPos = [self.backgroundBarPos[0] - self.backgroundBarScale[0] / 2 + self.backgroundBarScale[0] * self.threeStarPercent, self.backgroundBarPos[1], self.backgroundBarPos[2] + 2.0]
		self.tickScale = tickScale
		self.tickPath = tickPath

		self.oneStarTick = graphicsHelper.createSprite(self.tickScale[0], self.tickScale[1], self.tickPath)
		self.oneStarTick.position = vmath.vec3(self.oneStarTickPos)
		self.twoStarTick = graphicsHelper.createSprite(self.tickScale[0], self.tickScale[1], self.tickPath)
		self.twoStarTick.position = vmath.vec3(self.twoStarTickPos)
		self.threeStarTick = graphicsHelper.createSprite(self.tickScale[0], self.tickScale[1], self.tickPath)
		self.threeStarTick.position = vmath.vec3(self.threeStarTickPos)

		# UI parts
		self.showcase = showcase
		
		self.DisplayCurrentCompleteProgress()
		self.Display()
	
	def Update(self, currentProgress):
		self.percentComplete = currentProgress
		self.DisplayCurrentCompleteProgress()

	def DisplayCurrentCompleteProgress(self):
		self.sliderBarPos = [1.4 + self.backgroundBarPos[0] - self.backgroundBarScale[0] / 2 + (self.sliderBarScale[0] * self.percentComplete) / 2, self.backgroundBarPos[1] - 0.7, self.backgroundBarPos[2] + 1.0]
		sliderBarPercentScale = [self.percentComplete, 1]
		self.sliderBar.position = vmath.vec3(self.sliderBarPos)
		self.sliderBar.scale = vmath.vec3(sliderBarPercentScale)
	
	def Display(self):
		self.isDisable = False
		self.showcase.add(self.backgroundBar)
		self.showcase.add(self.sliderBar)
		self.showcase.add(self.oneStarTick)
		self.showcase.add(self.twoStarTick)
		self.showcase.add(self.threeStarTick)
	
	def Hide(self):
		self.isDisable = True
		self.showcase.remove(self.backgroundBar)
		self.showcase.remove(self.sliderBar)
		self.showcase.remove(self.oneStarTick)
		self.showcase.remove(self.twoStarTick)
		self.showcase.remove(self.threeStarTick)

