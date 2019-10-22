import pybullet as p
import time
import pybullet_data
from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
import math
import random
from power_button import PowerButton
from ui_manager import UIManager

from player import Player
from mapLevel import MapLevel
import json
class GameScene:
	def __init__(self):
		# Setting Pybullet
		p.connect(p.DIRECT)
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

		self.stepdt = 1 / FPS
		self.totalstepdt = 0
		p.setRealTimeSimulation(0)
		ddt = 1.0 / FPS
		
		# Create dictionary to store collision
		self.collision_objects = dict()

		# PYXIE SETTING REGION
		# =============================================================================================================
		self.cam = pyxie.camera('maincam')
		self.cam.lockon = True
		self.cam.position = vmath.vec3(0.0, -3.0, 3)
		self.cam.target = vmath.vec3(0.0, 0.0, 0.0)
		self.cam.farPlane = 250.0
		self.cam.fieldOfView = 80

		self.showcase = pyxie.showcase("case01")
		scale = vmath.vec3(10, 10, 10)
		position = vmath.vec3(0.0, -10.0, 3)
		player_col_scale = [0.1, 0.1, 1]
		player_col_local_pos = [0.0, 0.0, 1.1]
		self.player = Player(position, scale, [ 0, 0.7071068, 0.7071068, 0 ], 'asset/kuma_stand', self.cam, player_col_scale, player_col_local_pos, True)
		p.changeDynamics(player.colId, -1, linearDamping=100.0, lateralFriction=1, restitution=0.0)
		self.showcase.add(self.player.model)
		self.collision_objects[str(self.player.colId)] = self.player

		#UI showcase and camera
		self.UIshowcase = pyxie.showcase("UIcase")
		self.UIcam = pyxie.camera('UIcamera')
		self.UIcam.orthographicProjection = True
		self.UIcam.position = vmath.vec3(0.0, 0, 100)
		self.UIcam.target = vmath.vec3(0,0,0)
		self.UI_manager = UIManager()

		#Create button
		pos = [100,200,1]
		scale = [100, 50]
		powerUpButton = PowerButton(pos, scale, 'asset/cube_01', self.UIshowcase, self.UIcam, self.UI_manager)

		# Create map
		self.level = MapLevel('mapfiles/map.json', self.showcase, self.collision_objects)

		#DEBUG ON GUI MODE
		self.cameraDistance = 10
		self.cameraYaw = 0
		self.cameraPitch = -35
	
	def Update(self):
		if self.totalstepdt > self.stepdt:
			p.stepSimulation()
		while self.totalstepdt > self.stepdt:
			self.totalstepdt -= self.stepdt
	
		dt = pyxie.getElapsedTime()
		self.totalstepdt += dt
		
		touch = pyxie.singleTouch()
		if not touch or not touch['is_holded']:
			self.UI_manager.isTouchOnUI = False
		self.powerUpButton.Update(touch)
		self.player.update(touch, self.collision_objects, self.UI_manager)
		
		self.cam.shoot(self.showcase)
		self.UIcam.shoot(self.UIshowcase, clearColor=False)
		self.level.update(touch, self.player)

		playerPos, orn = p.getBasePositionAndOrientation(self.player.colId)

		cameraTargetPosition = playerPos
		p.resetDebugVisualizerCamera(self.cameraDistance, self.cameraYaw, self.cameraPitch, cameraTargetPosition)

	def OnExit(self):
		p.disconnect()

	def ResetScene(self):
		self.OnExit()
		self.__init__()