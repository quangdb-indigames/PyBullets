import json
from cell import Cell
class MapLevel():
	def __init__(self, filePath, showcase, collision_objects):
		self.showcase = showcase
		self.filePath = filePath
		self.collision_objects = collision_objects
		self.cell_list = []
		# Init
		# self.__initialize()

	def update(self, touch, player):
		for cell in self.cell_list:
			cell.update(touch)
		# self.__checkPlayerPosition(player)

	def __initialize(self):
		with open(self.filePath) as f:
			self.cell_list_data = json.load(f)
		
		self.length = self.cell_list_data[0]
		self.base_length = self.cell_list_data[0]
		for i in range(1, len(self.cell_list_data)):
			cell = Cell(self.cell_list_data[i]['cellPath'], self.showcase, self.collision_objects)
			self.cell_list.append(cell)
	
	def __checkPlayerPosition(self, player):
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
		self.cell_list.append(cell)
