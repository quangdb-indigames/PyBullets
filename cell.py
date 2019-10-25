import pybullet as p
import time
import pybullet_data
import pyxie
import pyvmath as vmath
import json
from cube import Cube
from cylinder import Cylinder
from obstacle import Obstacle


class Cell():
	def __init__(self, filePath, showcase, collision_objects, base_position = [0, 0, 0]):
		self.filePath = filePath
		self.showcase = showcase
		self.position = [0,0,0]
		self.scale = [1,1,1]
		self.objects = []
		self.obstacles = []
		self.collision_objects = collision_objects
		self.base_position = base_position
		self.__initialize()
		self.isDestroy = False
		
	def update(self, touch):
		if self.isDestroy:
			return

		if len(self.objects) > 0:
			for obj in self.objects:
				obj.update(touch)
		for obstacle in self.obstacles:
			obstacle.Update()

	def __initialize(self):
		# Load self.mapData from json file
		with open(self.filePath) as f:
			self.mapData = json.load(f)

		# Create background object
		self.position = [self.mapData['position'][0] + self.base_position[0], self.mapData['position'][1] + self.base_position[1], self.mapData['position'][2] + self.base_position[2] ]
		self.scale = self.mapData['scale']
		self.background = pyxie.figure(self.mapData['background']['path'])
		self.background.position = vmath.vec3(self.position)
		self.background.scale = vmath.vec3(self.scale)
		self.showcase.add(self.background)

		# Spawn all objects inside this cell
		if len(self.mapData['objects']) > 0:
			for obj in self.mapData['objects']:
				actual_obj = self.__spawnDependOnObjectType(obj)
				if actual_obj is not None:
					self.objects.append(actual_obj)

		# Create col box for background for check, will delete this part later
		col_scale = [self.scale[0] / 2, self.scale[1] / 2, self.scale[2] / 2]
		colId = p.createCollisionShape(p.GEOM_BOX, halfExtents=col_scale)
		self.multiId = p.createMultiBody(baseMass = 0, baseCollisionShapeIndex = colId, basePosition= self.position);

	# Spawn region
	def __spawnDependOnObjectType(self, obj):
		if obj['type'] == "BOX":
			actual_obj = self.__spawnBoxTypeObject(obj)
			return actual_obj

		if obj['type'] == "CYLINDER":
			actual_obj = self.__spawnCylinderTypeObject(obj)
			return actual_obj
			
	
	def __spawnBoxTypeObject(self, obj):
		pos = [self.position[0] + obj['local_pos'][0], self.position[1] + obj['local_pos'][1], self.position[2] + obj['local_pos'][2]]
		scale = obj['local_scale']
		model_path = obj['path']
		obj_col_pos = obj['col_pos']
		obj_col_scale = obj['col_scale']
		quat = obj['local_quaternion']
		isStatic = obj['isStatic']
		box = Cube(pos, scale, model_path, obj_col_scale, obj_col_pos, quat, isStatic)
		if 'canCollider' in obj and obj['canCollider'] == "TRUE":
			self.collision_objects[str(box.colId)] = box
		self.showcase.add(box.model)

		if 'isObstacle' in obj and obj['isObstacle']:
			self.CreateObstacle(box, obj)

		return box

	def __spawnCylinderTypeObject(self, obj):
		pos = [self.position[0] + obj['local_pos'][0], self.position[1] + obj['local_pos'][1], self.position[2] + obj['local_pos'][2]]
		scale = obj['local_scale']
		model_path = obj['path']
		obj_col_pos = obj['col_pos']
		quat = obj['local_quaternion']
		col_rad = obj['col_radius']
		col_height = obj['col_height']
		isStatic = obj['isStatic']
		cylinder = Cylinder(pos, scale, model_path, col_rad, col_height, obj_col_pos, quat, isStatic)
		if 'canCollider' in obj and obj['canCollider'] == "TRUE":
			self.collision_objects[str(cylinder.colId)] = cylinder
		self.showcase.add(cylinder.model)
		return cylinder
	
	def CreateObstacle(self, obj, objData):
		start_pos = [self.position[0] + objData['local_start_pos'][0], self.position[1] + objData['local_start_pos'][1], self.position[2] + objData['local_start_pos'][2]]
		end_pos = [self.position[0] + objData['local_end_pos'][0], self.position[1] + objData['local_end_pos'][1], self.position[2] + objData['local_end_pos'][2]]
		obstacle = Obstacle(obj, objData['move_speed'], start_pos, end_pos)
		self.obstacles.append(obstacle)

	def Destroy(self):
		self.isDestroy = True
		for obj in self.objects:
			self.showcase.remove(obj.model)
			p.removeBody(obj.colId)
		self.showcase.remove(self.background)
		p.removeBody(self.multiId)
		self.obstacles.clear()

	# End Region
			
