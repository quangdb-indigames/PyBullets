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
		if player.model.position.y >= 500 and self.state == STATE_PLAY:
			print("Finally!!!!")
			self.state = STATE_FINAL
			for cell in self.cell_list:
				cell.Destroy()
			self.collision_objects = []
			self.finalScene.ToActivateState()
			self.ResetPlayer(player)

		if self.state == STATE_FINAL:
			self.finalScene.Update()
			return
			
		curCell_Y = player.model.position.y / 30
		if curCell_Y >= self.length[1] - 9:
			# Auto spawn new map when player reach certain cell
			base_pos = [0, self.length[1] * 30, 0]
			for i in range(1, len(self.cell_list_data)):
				cell = Cell(self.cell_list_data[i]['cellPath'], self.showcase, self.collision_objects, base_pos)
				self.cell_list.append(cell)
			self.length = [self.length[0], self.length[1] + self.base_length[1]]
	
	def CreateACell(self, cellPath, pos):
		cell = Cell(cellPath, self.showcase, self.collision_objects, pos)
		# self.cell_list.append(cell)
	
	def ResetPlayer(self, player):
		pos, orn = p.getBasePositionAndOrientation(player.colId)
		linearVelocity, angularVelocity = p.getBaseVelocity(player.colId)
		newPos = [pos[0], -10, pos[2]]
		p.resetBasePositionAndOrientation(player.colId, newPos, orn)

		#Target
		target = [0, 30, 0]
		direction = [target[0] - newPos[0], target[1] - newPos[1], target[2] - newPos[2]]
		multiVelocity = vmath.length(vmath.vec3(linearVelocity))
		newVelocity = [direction[0] * multiVelocity * 0.005, direction[1] * multiVelocity * 0.005, direction[2] * multiVelocity * 0.005]
		p.resetBaseVelocity(player.colId, newVelocity, angularVelocity)
