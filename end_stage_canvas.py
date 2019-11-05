from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
from scene_manager import SceneManager
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
		self.ui_manager = ui_manager
		self.tapped = False

		# Board
		self.boardScale = boardScale
		self.boardPath = boardPath
		self.board = graphicsHelper.createSprite(self.boardScale[0], self.boardScale[1], self.boardPath)
		self.board.position = vmath.vec3(self.centerPos)

		# Clear Stage Text
		self.clearTextPos = [self.centerPos[0], self.centerPos[1] + 170, self.centerPos[2]]
		self.clearTextScale = clearStageTextScale
		self.clearTextPath = clearStageTextPath
		self.clearText = graphicsHelper.createSprite(self.clearTextScale[0], self.clearTextScale[1], self.clearTextPath)
		self.clearText.position = vmath.vec3(self.clearTextPos)

		# Star
		self.starScale = starScale
		self.whiteStarPath = whiteStarPath
		self.yellowStarPath = yellowStarPath
		self.listStar = list()

		# Next Button
		self.nextButtonPos = [self.centerPos[0] + 60, self.centerPos[1] - 100, self.centerPos[2]]
		self.nextButtonScale = buttonScale
		self.nextButtonPath = nextButtonPath
		self.nextButton = graphicsHelper.createSprite(self.nextButtonScale[0], self.nextButtonScale[1], self.nextButtonPath)
		self.nextButton.position = vmath.vec3(self.nextButtonPos)

		# Next Button
		self.retryButtonPos = [self.centerPos[0] - 60, self.centerPos[1] - 100, self.centerPos[2]]
		self.retryButtonScale = buttonScale
		self.retryButtonPath = retryButtonPath
		self.retryButton = graphicsHelper.createSprite(self.retryButtonScale[0], self.retryButtonScale[1], self.retryButtonPath)
		self.retryButton.position = vmath.vec3(self.retryButtonPos)
	
	def Update(self, touch):
		self.CheckOnClickRetryButton(touch)
	
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
		self.leftBasePos = [self.centerPos[0] - 90, self.centerPos[1] + 102, self.centerPos[2]]
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
			star.position = vmath.vec3([self.leftBasePos[0] + i * 45, self.leftBasePos[1], self.leftBasePos[2]])
			self.showcase.add(star)
			self.listStar.append(star)

	def CheckOnClickRetryButton(self, touch):
		if touch:
			if touch['is_holded']:			
				if self.CheckInsideRetryButton(touch) and not self.tapped:
					self.tapped = True
					self.ui_manager.isTouchOnUI = True
					self.OnClickRetryButtonExcute()
			else:
				self.tapped = False
		else:
			self.tapped = False
	
	def CheckInsideRetryButton(self, touch):
		direction = self.ConvertScreenToWorld(touch['cur_x'], touch['cur_y'], 0, self.camera)
		if direction.x <= self.retryButton.position.x + self.retryButtonScale[0] / 2 and direction.x >= self.retryButton.position.x - self.retryButtonScale[0] / 2 \
			and direction.y <= self.retryButton.position.y + self.retryButtonScale[1] / 2 and direction.y >= self.retryButton.position.y - self.retryButtonScale[1] / 2:
			return True
		return False
	
	def OnClickRetryButtonExcute(self):
		currentScene = SceneManager.GetCurrentScene()
		currentScene.resetDataButton.OnClickExcute()
		currentScene.SetState("STATE_RETRY")
	
	def ConvertScreenToWorld(self, scrx, scry, worldz, cam, w=None, h=None):
		invproj = vmath.inverse(cam.projectionMatrix)
		invview = cam.viewInverseMatrix
		if not w or not h:
			w, h = pyxie.viewSize()
		x = scrx / w * 2
		y = scry / h * 2

		pos = vmath.vec4(x, y, 0.0, 1.0)
		npos = invproj * pos
		npos = invview * npos
		npos.z /= npos.w
		npos.x /= npos.w
		npos.y /= npos.w
		npos.w = 1.0
		pos = vmath.vec4(x, y, 1.0, 1.0)
		fpos = invproj * pos
		fpos = invview * fpos
		fpos.z /= fpos.w
		fpos.x /= fpos.w
		fpos.y /= fpos.w
		fpos.w = 1.0

		dir = vmath.normalize(fpos - npos)
		return npos + (dir * (npos.z - worldz))
		



