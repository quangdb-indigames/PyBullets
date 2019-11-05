import json
import pybullet as p
from cell import Cell
import pyvmath as vmath
from finalScene import FinalScene
import pyxie
STATE_PLAY = "STATE_PLAY"
STATE_FINAL = "STATE_FINAL"

class MapLevel():
	def __init__(self, filePath, showcase, collision_objects, progress_bar, destroy_bar):
		self.showcase = showcase
		self.filePath = filePath
		self.collision_objects = collision_objects
		self.cell_list = []
		self.state = STATE_PLAY
		# Init
		self.__initialize()

		# For final scene
		self.finalScene = FinalScene(self.showcase)
		# self.finalScene.center[1] = 1100
		self.activeRange = 3
		self.firstFinalContact = False
		self.reduceVelocity = False

		# For moving camera on final
		self.isOnFinalCam = False
		self.minFarCam = 1475
		self.maxHighCam = 25
		self.finalCamTarget = [0, 1500, 10]

		# For progress bar supporting
		self.progress_bar = progress_bar
		self.destroy_bar = destroy_bar
		self.startProgressPos = -10
		self.finalProgressPos = 1400
		self.totalProgressDis = self.finalProgressPos - self.startProgressPos - 50
		self.currentProgress = 0.01


	def update(self, touch, player):
		for cell in self.cell_list:
			cell.update(touch)
		self.__checkPlayerPosition(player)
		if self.state == STATE_PLAY:
			self.CalculateCurrentProgress(player)

		self.progress_bar.Update(self.currentProgress, self)
		if not self.destroy_bar.isDisable:
			destroyPercent = self.CalculateDestroyProgress()
			self.destroy_bar.Update(destroyPercent)

		if self.isOnFinalCam:
			self.CameraOnFinal(player)

	def CalculateCurrentProgress(self, player):
		flyedDis = player.model.position.y - self.startProgressPos
		percentProgress = round(flyedDis / self.totalProgressDis, 5)
		if percentProgress < 0.01:
			percentProgress = 0.01
		elif percentProgress > 1.0:
			percentProgress = 1.0
		self.currentProgress = percentProgress
	
	def CalculateDestroyProgress(self):
		percent = self.finalScene.GetDestroyPercent()
		return round(percent, 5)

	def __initialize(self):
		with open(self.filePath) as f:
			self.cell_list_data = json.load(f)

		self.length = len(self.cell_list_data[0])
		self.base_length = len(self.cell_list_data[0])
		self.ConstructCellFromData([0,0,0])

	def __checkPlayerPosition(self, player):
		if player.model.position.y >= self.finalProgressPos - 50 and self.progress_bar.onAlert == False:
			self.progress_bar.onAlert = True

		if player.model.position.y >= self.finalProgressPos and self.state == STATE_PLAY:
			self.state = STATE_FINAL
			self.finalScene.ToActivateState()
			if self.progress_bar.isDisable:
				self.destroy_bar.Display()	
		
		if player.model.position.y >= 1490:
			player.camFollow = False
			self.isOnFinalCam = True

		if self.state == STATE_FINAL:
			self.CheckInsideActiveRange(player)
			self.finalScene.Update()
			self.CheckContact(player)
			self.CheckReduceVelocity(player)
			# self.StaticMoveOnFinal(player)
			return

		curCell_Y = player.model.position.y / 30
		if curCell_Y >= self.length - 9:
			# Auto spawn new map when player reach certain cell
			base_pos = [0, self.length * 30, 0]
			self.ConstructCellFromData(base_pos)
			self.length = self.length + self.base_length
			if len(self.cell_list) > 22:
				new_list = list()
				for cell in self.cell_list:
					if player.model.position.y - 80 > cell.position[1]:
						cell.Destroy()
					else:
						new_list.append(cell)
				self.cell_list = new_list
	
	def ConstructCellFromData(self, base_pos):
		for cell_col in self.cell_list_data:
			for cell_data in cell_col:
				cell = Cell(cell_data, self.showcase, self.collision_objects, base_pos)
				self.cell_list.append(cell)

	def CameraOnFinal(self, player):
		if player.cam.position.z < self.maxHighCam:
			newPos = [player.cam.position.x, player.cam.position.y, player.cam.position.z + 0.1]
			player.cam.position = vmath.vec3(newPos)
		if player.cam.position.y > self.minFarCam:
			newPos = [player.cam.position.x, player.cam.position.y - 0.2, player.cam.position.z]
			player.cam.position = vmath.vec3(newPos)
		player.cam.target = vmath.vec3(self.finalCamTarget)


	def CheckReduceVelocity(self, player):
		if self.firstFinalContact and self.reduceVelocity == False:
			self.reduceVelocity = True
			linearVelocity, angularVelocity = p.getBaseVelocity(player.colId)
			platform = pyxie.getPlatform()
			if platform == pyxie.TARGET_PLATFORM_ANDROID:
				newVelocity = [linearVelocity[0] / 5, linearVelocity[1] / 5, linearVelocity[2] / 5]
			else:
				newVelocity = [linearVelocity[0] / 2, linearVelocity[1] / 2, linearVelocity[2] / 2]
			p.resetBaseVelocity(player.colId, newVelocity, angularVelocity)

	def CheckInsideActiveRange(self, player):
		player_pos, player_orn = p.getBasePositionAndOrientation(player.colId)
		for bd in self.finalScene.bodies:
			if not bd or bd in self.finalScene.activatedBodies:
				continue

			pos, orn = p.getBasePositionAndOrientation(bd)
			distanceVec = [player_pos[0] - pos[0], player_pos[1] - pos[1], player_pos[2] - pos[2]]
			distance = vmath.length(vmath.vec3(distanceVec))
			if distance < self.activeRange:
				# Then activate bd
				p.changeDynamics(bodyUniqueId=bd, linkIndex=-1, mass=5)
				self.finalScene.activatedBodies.append(bd)

	def CheckContact(self, player):
		aabbMin, aabbMax = p.getAABB(player.colId, -1)
		collision_list = p.getOverlappingObjects(aabbMin, aabbMax)
		if collision_list is not None and len(collision_list) != 0:
			for objId in collision_list:
				colId = objId[0]
				if colId != 0 and colId in self.finalScene.activatedBodies:
					self.firstFinalContact = True
					break


	def CreateACell(self, cellPath, pos):
		cell = Cell(cellPath, self.showcase, self.collision_objects, pos)
		# self.cell_list.append(cell)

	def StaticMoveOnFinal(self, player):
		linearVelocity, angularVelocity = p.getBaseVelocity(player.colId)
		p.resetBaseVelocity(player.colId, self.finalVelocity, angularVelocity)

	def ResetPlayer(self, player):
		pos, orn = p.getBasePositionAndOrientation(player.colId)
		linearVelocity, angularVelocity = p.getBaseVelocity(player.colId)
		newPos = [0, 0, pos[2]]
		p.resetBasePositionAndOrientation(player.colId, newPos, orn)

		#Target
		target = [0, 30, 2]
		direction = [target[0] - newPos[0], target[1] - newPos[1], target[2] - newPos[2]]
		multiVelocity = vmath.length(vmath.vec3(linearVelocity))
		self.finalVelocity = newVelocity = [direction[0] * multiVelocity * 0.05, direction[1] * multiVelocity * 0.05, direction[2] * multiVelocity * 0.05]
		p.resetBaseVelocity(player.colId, newVelocity, angularVelocity)
	
	def SaveResult(self):
		"""
		This will save all activated body into a file.\n
		In next game loop, this final scene will read data from it and won't update\n
		any body in it.
		"""
		if self.state == STATE_FINAL:
			self.finalScene.SaveResult()
	
	def Destroy(self):
		if self.state == STATE_FINAL:
			self.finalScene.Destroy()

