import pybullet as p
import time
import pybullet_data
from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
import math
import random

from player import Player
from mapLevel import MapLevel
import json

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
pyxie.window(True, SCREEN_WIDTH , SCREEN_HEIGHT)

physicsClient = p.connect(p.DIRECT)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
boxHalfLength = 0.5
boxHalfWidth = 0.5
boxHalfHeight = 0.5
segmentLength = 5
# Create dictionary to store collision
collision_objects = dict()

# PYXIE SETTING REGION
# =============================================================================================================
cam = pyxie.camera('maincam')
cam.lockon = True
cam.position = vmath.vec3(0.0, -3.0, 3)
cam.target = vmath.vec3(0.0, 0.0, 0.0)
cam.farPlane = 250.0
cam.fieldOfView = 80

showcase = pyxie.showcase("case01")
scale = vmath.vec3(10, 10, 10)
position = vmath.vec3(0.0, -10.0, 3)
player_col_scale = [0.1, 0.1, 1]
player_col_local_pos = [0.0, 0.0, 1.1]
player = Player(position, scale, [ 0, 0.7071068, 0.7071068, 0 ], 'asset/kuma_stand', cam, player_col_scale, player_col_local_pos, True)
p.changeDynamics(player.colId, -1, linearDamping=100.0, lateralFriction=1, restitution=0.0)
showcase.add(player.model)
collision_objects[str(player.colId)] = player

# Create map
level = MapLevel('mapfiles/map.json', showcase, collision_objects)

# plane_colId = p.createCollisionShape(p.GEOM_PLANE)
# plane_boxId = p.createMultiBody(baseMass = 0, baseCollisionShapeIndex = plane_colId, basePosition= [0, 0, 0]);

p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -10)
FPS = 60
p.setPhysicsEngineParameter(
	fixedTimeStep=1.0 / FPS,
	numSolverIterations=12,
	numSubSteps=3,  # 8 is smooth but not sure abt performance. Lowered substeps actually raise fps
	contactBreakingThreshold=0.00000002,
	useSplitImpulse=0,
	splitImpulsePenetrationThreshold=9999999,
	enableConeFriction=0,
	deterministicOverlappingPairs=0,
	solverResidualThreshold=0.1,
)

stepdt = 1 / FPS
totalstepdt = 0
p.setRealTimeSimulation(0)
ddt = 1.0 / FPS

cameraDistance = 10
cameraYaw = 0
cameraPitch = -35

isRotate = False
while(1):
	if totalstepdt > stepdt:
		p.stepSimulation()
		while totalstepdt > stepdt:
			totalstepdt -= stepdt
	
	dt = pyxie.getElapsedTime()
	totalstepdt += dt
	
	touch = pyxie.singleTouch()
	player.update(touch, collision_objects)
	cam.shoot(showcase)
	level.update(touch, player)
	pyxie.swap()

	playerPos, orn = p.getBasePositionAndOrientation(player.colId)

	cameraTargetPosition = playerPos
	p.resetDebugVisualizerCamera(cameraDistance, cameraYaw, cameraPitch, cameraTargetPosition)
