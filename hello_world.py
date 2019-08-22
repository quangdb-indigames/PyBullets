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

def getRayFromTo(mouseX, mouseY):
	
  width, height, viewMat, projMat, cameraUp, camForward, horizon, vertical, _, _, dist, camTarget = p.getDebugVisualizerCamera(
  )
  camPos = [
	  camTarget[0] - dist * camForward[0], camTarget[1] - dist * camForward[1],
	  camTarget[2] - dist * camForward[2]
  ]
  farPlane = 10000
  rayForward = [(camTarget[0] - camPos[0]), (camTarget[1] - camPos[1]), (camTarget[2] - camPos[2])]
  invLen = farPlane * 1. / (math.sqrt(rayForward[0] * rayForward[0] + rayForward[1] *
									  rayForward[1] + rayForward[2] * rayForward[2]))
  rayForward = [invLen * rayForward[0], invLen * rayForward[1], invLen * rayForward[2]]
  rayFrom = camPos
  oneOverWidth = float(1) / float(width)
  oneOverHeight = float(1) / float(height)
  dHor = [horizon[0] * oneOverWidth, horizon[1] * oneOverWidth, horizon[2] * oneOverWidth]
  dVer = [vertical[0] * oneOverHeight, vertical[1] * oneOverHeight, vertical[2] * oneOverHeight]
  rayToCenter = [
	  rayFrom[0] + rayForward[0], rayFrom[1] + rayForward[1], rayFrom[2] + rayForward[2]
  ]
  rayTo = [
	  rayToCenter[0] - 0.5 * horizon[0] + 0.5 * vertical[0] + float(mouseX) * dHor[0] -
	  float(mouseY) * dVer[0], rayToCenter[1] - 0.5 * horizon[1] + 0.5 * vertical[1] +
	  float(mouseX) * dHor[1] - float(mouseY) * dVer[1], rayToCenter[2] - 0.5 * horizon[2] +
	  0.5 * vertical[2] + float(mouseX) * dHor[2] - float(mouseY) * dVer[2]
  ]
  return rayFrom, rayTo


SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
pyxie.window(True, SCREEN_WIDTH , SCREEN_HEIGHT)

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
boxHalfLength = 0.5
boxHalfWidth = 0.5
boxHalfHeight = 0.5
segmentLength = 5

# PYXIE SETTING REGION
# =============================================================================================================
cam = pyxie.camera('maincam')
cam.lockon = True
cam.position = vmath.vec3(0.0, -3.0, 3)
cam.target = vmath.vec3(0.0, 0.0, 0.0)

showcase = pyxie.showcase("case01")
scale = vmath.vec3(1, 1, 1)
position = vmath.vec3(0.0, 0.0, 3)
player_col_scale = [0.2,0.2,0.8]
player_col_local_pos = [0, 0, 0.9]
player = Player(position, scale, [ 0, 0.7071068, 0.7071068, 0 ], 'asset/Sapphiart', cam, player_col_scale, player_col_local_pos, True)

showcase.add(player.model)
# Rotate
# dx = -90.0
# dy = 10.0  # -150
# dz = -10.0	 # 180
# vect = vmath.normalize((dx, dy, dz))
# player.model.rotation = vmath.normalize(vmath.quat_rotation((1, 0, 0), vect))
# player.model.rotation = vmath.quat([ 0, 0.6427876, 0.7660444, 0 ])
# print(player.model.rotation)

# dx = 360.0
# dy = 0.0
# dz = 0.0
# vect = vmath.normalize((dx, dy, dz))
# cube.model.rotation = vmath.normalize(vmath.quat_rotation((1, 0, 0), vect))
# cube2_pos = vmath.vec3(4.0, 5.0, 0.0)
# cube2_scale = vmath.vec3(1, 1, 1)
# cube2 = Cube(cube2_pos, cube2_scale, 'asset/plane', cam, True)
# showcase.add(cube2.model)

# Create plane
position = vmath.vec3(-10.0, 0.0, 0.0)
scale = vmath.vec3(10, 10, 0.1)
plane_col_scale = [10, 10, 0.1]
plane = Plane(position, 'asset/plane', 5, scale, showcase)

# Create cube
position = vmath.vec3(0.0, 8.0, 2.0)
scale = vmath.vec3(1, 1, 1)
cube_col_scale = [1, 1, 1]
cube = Cube(position, scale, 'asset/cube_02', cube_col_scale, [0, 0, -0.4])
cube.model.rotation = vmath.quat([ 0, 0, 0, 1 ])
showcase.add(cube.model)

# colBoxId = p.createCollisionShape(p.GEOM_BOX,
# 								  halfExtents=[boxHalfLength, boxHalfWidth, boxHalfHeight])

# boxId = p.createMultiBody(baseMass = 1, baseCollisionShapeIndex = colBoxId, basePosition= [0.0, 0.0, 3.0]);
# p.changeVisualShape(colBoxId, -1, rgbaColor=[0.5, 0.1, 0.7, 1])

p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -10)
# planeId = p.loadURDF("plane.urdf")
# p.changeDynamics(colBoxId, -1, linearDamping=5.0, lateralFriction=1, restitution=0.0)
# cubeStartPos = [0, 0, 1]
# cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
# boxId = p.loadURDF("r2d2.urdf", cubeStartPos, cubeStartOrientation)
cameraDistance = 10
cameraYaw = 0
cameraPitch = -35

isRotate = False
while(1):
	p.stepSimulation()
	time.sleep(1. / 240.)
	touch = pyxie.singleTouch()
	player.update(touch)
	cam.shoot(showcase)
	cube.update(touch)
	pyxie.swap()

	playerPos, orn = p.getBasePositionAndOrientation(player.colBoxId)

	cameraTargetPosition = playerPos
	p.resetDebugVisualizerCamera(cameraDistance, cameraYaw, cameraPitch, cameraTargetPosition)


	# pos, orn = p.getBasePositionAndOrientation(colBoxId)
	# cameraTargetPosition = pos
	# p.resetDebugVisualizerCamera(cameraDistance, cameraYaw, cameraPitch, cameraTargetPosition)

	# forward = 0
	# mouseEvents = p.getMouseEvents()
	# camInfo = p.getDebugVisualizerCamera()
	# camForward = camInfo[5]
	# for e in mouseEvents:
	# 	if ((e[0] == 2) and (e[3] == 0) and (e[4] & p.KEY_WAS_TRIGGERED)):
	# 		mouseX = e[1]
	# 		mouseY = e[2]
	# 		rayFrom, rayTo = getRayFromTo(mouseX, mouseY)
	# 		rayInfo = p.rayTest(rayFrom, rayTo)
	# 		for l in range(len(rayInfo)):
	# 			hit = rayInfo[l]
	# 			objectUid = hit[0]
	# 			if(objectUid >= 0):
	# 				p.changeVisualShape(objectUid, -1, rgbaColor=[random.random(), random.random(), random.random(), 1])
	# 				pos, orn = p.getBasePositionAndOrientation(objectUid)
	# 				print(pos)
	# 				p.applyExternalForce(objectUid, -1, forceObj=[0.0, 0.0, 1000.0], posObj=[pos[0], pos[1], pos[2] + 1], flags=p.WORLD_FRAME)
	# 				break
	# keys = p.getKeyboardEvents()
	# for k, v in keys.items():
	# 	if(k == p.B3G_UP_ARROW and (v & p.KEY_WAS_TRIGGERED)):
	# 		forward = 1
	# 	if(k == p.B3G_UP_ARROW and (v & p.KEY_WAS_RELEASED)):
	# 			forward = 0
	# force = [camForward[0] * 1000.0, camForward[1] * 1000.0, 2000]
	# if(forward):
	# 	print(camForward)
	# 	pos, orn = p.getBasePositionAndOrientation(colBoxId)
	# 	p.applyExternalForce(colBoxId, -1, force, pos, flags = p.WORLD_FRAME)



