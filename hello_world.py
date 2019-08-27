import pybullet as p
import time
import pybullet_data
from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
import math
import random
from cube import Cube
from player import Player
from plane import Plane
import json


with open('cell_01.json') as f:
	cell_01 = json.load(f)
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
pyxie.window(True, SCREEN_WIDTH , SCREEN_HEIGHT)

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
boxHalfLength = 0.5
boxHalfWidth = 0.5
boxHalfHeight = 0.5
segmentLength = 5
# Create dictionary to store collision
obj_list = dict()

# PYXIE SETTING REGION
# =============================================================================================================
cam = pyxie.camera('maincam')
cam.lockon = True
cam.position = vmath.vec3(0.0, -3.0, 3)
cam.target = vmath.vec3(0.0, 0.0, 0.0)

showcase = pyxie.showcase("case01")
scale = vmath.vec3(1, 1, 1)
position = vmath.vec3(0.0, 0.0, 3)
player_col_scale = [0.1,0.1,0.8]
player_col_local_pos = [0, 0, 0.9]
player = Player(position, scale, [ 0, 0.7071068, 0.7071068, 0 ], 'asset/Sapphiart', cam, player_col_scale, player_col_local_pos, True)
p.changeDynamics(player.colBoxId, -1, linearDamping=100.0, lateralFriction=1, restitution=0.0)
showcase.add(player.model)
obj_list[str(player.colBoxId)] = player

# Create plane
position = vmath.vec3(-10.0, 0.0, 0.0)
scale = vmath.vec3(10, 10, 0.1)
plane_col_scale = [10, 10, 0.1]
plane = Plane(position, 'asset/plane_02', 10, scale, showcase)

# Create cube
position = vmath.vec3(0.0, 8.0, 2.0)
scale = vmath.vec3(2, 2, 2)
cube_col_scale = [1, 1, 1]
cube = Cube(position, scale, 'asset/cube_02', cube_col_scale, [0, 0, 0])
cube.model.rotation = vmath.quat([ 0, 0, 0, 1 ])
showcase.add(cube.model)
obj_list[str(cube.colBoxId)] = cube

maps_objs = []
# Create chair from json data
for obj in cell_01['objects']:
	pos = obj['local_pos']
	scale = obj['local_scale']
	model_path = obj['path']
	obj_col_pos = obj['col_pos']
	obj_col_scale = obj['col_scale']
	quat = obj['local_quaternion']
	chair = Cube(pos, scale, model_path, obj_col_scale, obj_col_pos, quat)
	showcase.add(chair.model)
	maps_objs.append(chair)

p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -50)

cameraDistance = 10
cameraYaw = 0
cameraPitch = -35

isRotate = False
print(len(maps_objs))
while(1):
	p.stepSimulation()
	time.sleep(1. / 240.)
	touch = pyxie.singleTouch()
	player.update(touch, obj_list)
	cam.shoot(showcase)
	cube.update(touch)
	for obj in maps_objs:
		obj.update(touch)
	pyxie.swap()

	playerPos, orn = p.getBasePositionAndOrientation(player.colBoxId)

	cameraTargetPosition = playerPos
	p.resetDebugVisualizerCamera(cameraDistance, cameraYaw, cameraPitch, cameraTargetPosition)
