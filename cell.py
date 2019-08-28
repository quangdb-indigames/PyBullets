import pybullet as p
import time
import pybullet_data
import pyxie
import pyvmath as vmath
import json
from cube import Cube
from cylinder import Cylinder

class Cell():
	def __init__(self, filePath, showcase, collision_objects):
		self.filePath = filePath
		self.showcase = showcase
		self.position = [0,0,0]
		self.scale = [1,1,1]
		self.objects = []
		self.collision_objects = collision_objects
		self.__initialize()

	def update(self, touch):
		if len(self.objects) > 0:
			for obj in self.objects:
				obj.update(touch)

	def __initialize(self):
		# Load data from json file
		with open(self.filePath) as f:
			data = json.load(f)

		# Create background object
		self.position = data['position']
		self.scale = data['scale']
		self.background = pyxie.figure(data['background']['path'])
		self.background.position = vmath.vec3(self.position)
		self.background.scale = vmath.vec3(self.scale)
		self.showcase.add(self.background)

		# Spawn all objects inside this cell
		if len(data['objects']) > 0:
			for obj in data['objects']:
				actual_obj = self.__spawnDependOnObjectType(obj)
				if actual_obj is not None:
					self.objects.append(actual_obj)

		# Create col box for background for check, will delete this part later
		col_scale = [self.scale[0] / 2, self.scale[1] / 2, self.scale[2] / 2]
		colId = p.createCollisionShape(p.GEOM_BOX, halfExtents=col_scale)
		p.createMultiBody(baseMass = 0, baseCollisionShapeIndex = colId, basePosition= self.position);

	def __spawnDependOnObjectType(self, obj):
		if obj['type'] == "BOX":
			pos = [self.position[0] + obj['local_pos'][0], self.position[1] + obj['local_pos'][1], self.position[2] + obj['local_pos'][2]]
			scale = obj['local_scale']
			model_path = obj['path']
			obj_col_pos = obj['col_pos']
			obj_col_scale = obj['col_scale']
			quat = obj['local_quaternion']
			isStatic = obj['isStatic']
			chair = Cube(pos, scale, model_path, obj_col_scale, obj_col_pos, quat, isStatic)
			self.showcase.add(chair.model)
			return chair

		if obj['type'] == "CYLINDER":
			pos = [self.position[0] + obj['local_pos'][0], self.position[1] + obj['local_pos'][1], self.position[2] + obj['local_pos'][2]]
			scale = obj['local_scale']
			model_path = obj['path']
			obj_col_pos = obj['col_pos']
			quat = obj['local_quaternion']
			col_rad = obj['col_radius']
			col_height = obj['col_height']
			isStatic = obj['isStatic']
			cylinder = Cylinder(pos, scale, model_path, col_rad, col_height, obj_col_pos, quat, isStatic)
			if obj['canCollider'] == "TRUE":
				self.collision_objects[str(cylinder.colId)] = cylinder
			self.showcase.add(cylinder.model)
			return cylinder
			
