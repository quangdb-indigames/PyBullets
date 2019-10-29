import json
import pybullet as p
from cell import Cell
import pyvmath as vmath
from finalScene import FinalScene
STATE_PLAY = "STATE_PLAY"
STATE_FINAL = "STATE_FINAL"
class MapLevel():
	def __init__(self, filePath, showcase, collision_objects):
		self.showcase = showcase
		self.filePath = filePath
		self.collision_objects = collision_objects
		self.cell_list = []
		self.state = STATE_PLAY
		# Init
		self.__initialize()

		# For final scene
		self.finalScene = FinalScene(self.showcase)
		self.activatedBodies = []
		self.activeRange = 2
		self.firstFinalContact = False
		self.reduceVelocity = False

	def update(self, touch, player):
		for cell in self.cell_list:
			cell.update(touch)
		self.__checkPlayerPosition(player)

	def __initialize(self):
		with open(self.filePath) as f:
			self.cell_list_data = json.load(f)
		
		self.length = self.cell_list_data[0]
		self.base_length = self.cell_list_data[0]
		for i in range(1, len(self.cell_list_data)):
			cell = Cell(self.cell_list_data[i]['cellPath'], self.showcase, self.collision_objects)
			self.cell_list.append(cell)
	
	def __checkPlayerPosition(self, player):
		if player.model.position.y >= 1200 and self.state == STATE_PLAY:
			self.state = STATE_FINAL
			for cell in self.cell_list:
				cell.Destroy()
			self.collision_objects = []
			self.finalScene.ToActivateState()
			self.CreateACell("mapfiles/final_cell.json", [0,0,0])
			self.ResetPlayer(player)
			player.abortCheckContact = True

		if self.state == STATE_FINAL:
			self.CheckInsideActiveRange(player)
			self.finalScene.Update()
			self.CheckContact(player)
			self.CheckReduceVelocity(player)
			# self.StaticMoveOnFinal(player)
			return
			
		curCell_Y = player.model.position.y / 30
		if curCell_Y >= self.length[1] - 9:
			# Auto spawn new map when player reach certain cell
			base_pos = [0, self.length[1] * 30, 0]
			for i in range(1, len(self.cell_list_data)):
				cell = Cell(self.cell_list_data[i]['cellPath'], self.showcase, self.collision_objects, base_pos)
				self.cell_list.append(cell)
			self.length = [self.length[0], self.length[1] + self.base_length[1]]

	def CheckReduceVelocity(self, player):
		if self.firstFinalContact and self.reduceVelocity == False:
			self.reduceVelocity = True
			linearVelocity, angularVelocity = p.getBaseVelocity(player.colId)
			newVelocity = [linearVelocity[0] / 2, linearVelocity[1] / 2, linearVelocity[2] / 2]
			p.resetBaseVelocity(player.colId, newVelocity, angularVelocity)

	def CheckInsideActiveRange(self, player):
		player_pos, player_orn = p.getBasePositionAndOrientation(player.colId)
		for bd in self.finalScene.bodies:
			if bd in self.activatedBodies:
				continue
			
			pos, orn = p.getBasePositionAndOrientation(bd)
			distanceVec = [player_pos[0] - pos[0], player_pos[1] - pos[1], player_pos[2] - pos[2]]
			distance = vmath.length(vmath.vec3(distanceVec))
			if distance < self.activeRange:
				# Then activate bd
				p.changeDynamics(bodyUniqueId=bd, linkIndex=-1, mass=1)
				self.activatedBodies.append(bd)
				
	def CheckContact(self, player):
		aabbMin, aabbMax = p.getAABB(player.colId, -1)
		collision_list = p.getOverlappingObjects(aabbMin, aabbMax)
		if collision_list is not None and len(collision_list) != 0:		
			for objId in collision_list:
				colId = objId[0]
				if colId != 0 and colId in self.activatedBodies:
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
