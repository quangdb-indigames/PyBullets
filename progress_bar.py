from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
from scene_manager import SceneManager
class ProgressBar():
	def __init__(self, pos, backgroundBarScale, sliderBarScale, sliderScale, backgroundBarPath, sliderBarPath, sliderNormalPath, sliderAlertPath, showcase):
		# Supporting attribute
		self.percentComplete = 0.05
		self.onFlying = True
		
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

		# Slider
		self.sliderPos = [self.backgroundBarPos[0] - self.backgroundBarScale[0] / 2 + (self.sliderBarScale[0] * self.percentComplete), self.backgroundBarPos[1], self.backgroundBarPos[2] + 2.0]
		self.sliderScale = sliderScale
		self.sliderNormalPath = sliderNormalPath
		self.sliderAlertPath = sliderAlertPath
		self.slider = graphicsHelper.createSprite(self.sliderScale[0], self.sliderScale[1], self.sliderNormalPath)
		self.slider.position = vmath.vec3(self.sliderPos)

		# UI parts
		self.showcase = showcase

		# Add to showcase
		self.showcase.add(self.backgroundBar)
		self.showcase.add(self.sliderBar)
		self.showcase.add(self.slider)

		self.DisplayCurrentCompleteProgress()
	
	def Update(self, currentProgress):
		if self.onFlying:
			self.percentComplete = currentProgress
			# if self.percentComplete < 1.0:
			# 	self.percentComplete += 0.01
			self.DisplayCurrentCompleteProgress()

	def DisplayCurrentCompleteProgress(self):
		self.sliderBarPos = [1.4 + self.backgroundBarPos[0] - self.backgroundBarScale[0] / 2 + (self.sliderBarScale[0] * self.percentComplete) / 2, self.backgroundBarPos[1] - 0.7, self.backgroundBarPos[2] + 1.0]
		sliderBarPercentScale = [self.percentComplete, 1]
		self.sliderBar.position = vmath.vec3(self.sliderBarPos)
		self.sliderBar.scale = vmath.vec3(sliderBarPercentScale)

		self.sliderPos = [1.4 + self.backgroundBarPos[0] - self.backgroundBarScale[0] / 2 + (self.sliderBarScale[0] * self.percentComplete), self.backgroundBarPos[1] - 0.7, self.backgroundBarPos[2] + 2.0]
		self.slider.position = vmath.vec3(self.sliderPos)

