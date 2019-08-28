import json
from cell import Cell
class MapLevel():
	def __init__(self, filePath, showcase, collision_objects):
		self.showcase = showcase
		self.filePath = filePath
		self.collision_objects = collision_objects
		self.cell_list = []
		# Init
		self.__initialize()

	def update(self, touch):
		for cell in self.cell_list:
			cell.update(touch)

	def __initialize(self):
		with open(self.filePath) as f:
			cell_list_data = json.load(f)
		
		for data in cell_list_data:
			cell = Cell(data['cellPath'], self.showcase, self.collision_objects)
			self.cell_list.append(cell)
