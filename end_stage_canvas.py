from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
THREE_STAR_RATE = "THREE_STAR_RATE"
TWO_STAR_RATE = "TWO_STAR_RATE"
ONE_STAR_RATE = "ONE_STAR_RATE"
UNCLEAR = "UNCLEAR"
class EndStageCanvas:
	def __init__(self, centerPos, boardScale, clearStageTextScale, starScale, buttonScale, boardPath, clearStageTextPath, whiteStarPath, yellowStarPath, nextButtonPath, retryButtonPath, showcase, camera, ui_manager):
		# Support attribute
		self.centerPos = centerPos
		self.isDisable = True
		self.showcase = showcase
		self.camera = camera
		self.UI_manager = ui_manager

		# Board
		self.boardScale = boardScale
		self.boardPath = boardPath
		self.board = graphicsHelper.createSprite(self.boardScale[0], self.boardScale[1], self.boardPath)
		self.board.position = vmath.vec3(self.centerPos)

		# Clear Stage Text
		self.clearTextPos = [self.centerPos[0], self.centerPos[1] + 100, self.centerPos[2]]
		self.clearTextScale = clearStageTextScale
		self.clearTextPath = clearStageTextPath
		self.clearText = graphicsHelper.createSprite(self.clearTextScale[0], self.clearTextScale[1], self.clearTextPath)

		# Star
		self.starScale = starScale
		self.whiteStarPath = whiteStarPath
		self.yellowStarPath = yellowStarPath
		self.listStar = list()

		# Next Button
		self.nextButtonPos = [self.centerPos[0] + 30, self.centerPos[1] - 70, self.centerPos[2]]
		self.nextButtonScale = buttonScale
		self.nextButtonPath = nextButtonPath
		self.nextButton = graphicsHelper.createSprite(self.nextButtonScale[0], self.nextButtonScale[1], self.nextButtonPath)

		# Next Button
		self.retryButtonPos = [self.centerPos[0] - 30, self.centerPos[1] - 70, self.centerPos[2]]
		self.retryButtonScale = buttonScale
		self.retryButtonPath = retryButtonPath
		self.retryButton = graphicsHelper.createSprite(self.retryButtonScale[0], self.retryButtonScale[1], self.retryButtonPath)
	
	def Display(self, rateType):
		self.isDisable = False
		self.showcase.add(self.board)
		self.showcase.add(self.clearText)
		self.showcase.add(self.nextButton)
		self.showcase.add(self.retryButton)
		self.DisplayStarRate(rateType)

	def Hide(self):
		self.isDisable = True
		self.showcase.remove(self.board)
		self.showcase.remove(self.clearText)
		self.showcase.remove(self.nextButton)
		self.showcase.remove(self.retryButton)
		for star in self.listStar:
			self.showcase.remove(star)
		self.listStar.clear()

	def DisplayStarRate(self, rateType):
		self.leftBasePos = [self.centerPos[0] - 60, self.centerPos[1] + 70, self.centerPos[2]]
		clearRate = -1
		if rateType == UNCLEAR:
			clearRate = -1
		elif rateType == ONE_STAR_RATE:
			clearRate = 1
		elif rateType == TWO_STAR_RATE:
			clearRate = 2
		elif rateType == THREE_STAR_RATE:
			clearRate = 3
		
		for i in range(1, 4):
			if i > clearRate:
				displayStar = self.whiteStarPath
			else:
				displayStar = self.yellowStarPath
			star = graphicsHelper.createSprite(self.starScale[0], self.starScale[1], displayStar)
			star.position = vmath.vec3([self.leftBasePos[0] + i * 30, self.leftBasePos[1], self.leftBasePos[2]])
			self.showcase.add(star)
			self.listStar.append(star)
		



