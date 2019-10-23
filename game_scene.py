import pybullet as p
import time
import pybullet_data
from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
import math
import random
from power_button import PowerButton
from replay_button import ReplayButton
from ui_manager import UIManager
from cannon import Cannon
from finalScene import FinalScene

from player import Player
from mapLevel import MapLevel
import json
class GameScene:
	def __init__(self):
		self.Init()

	def Init(self):
		# Setting Pybullet
		p.connect(p.GUI)
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

		#Init state
		self.state = "Initing"
		self.initDt = 0
		
		# Create dictionary to store collision
		self.collision_objects = dict()

		# PYXIE SETTING REGION
		# =============================================================================================================
		self.cam = pyxie.camera('maincam###' + str(random.randrange(1000)))
		self.cam.lockon = True
		self.cam.position = vmath.vec3(0.0, -3.0, 3)
		self.cam.target = vmath.vec3(0.0, 0.0, 0.0)
		self.cam.farPlane = 250.0
		self.cam.fieldOfView = 80

		self.showcase = pyxie.showcase("case01##" + str(random.randrange(1000)))
		scale = vmath.vec3(10, 10, 10)
		position = vmath.vec3(0.0, -10.0, 0.75)
		player_col_scale = [0.1, 0.1, 1]
		player_col_local_pos = [0.0, 0.0, 1.1]
		self.player = Player(position, scale, [ 0, 0.7071068, 0.7071068, 0 ], 'asset/Betakkuma/betakkuma', self.cam, player_col_scale, player_col_local_pos, True)
		p.changeDynamics(self.player.colId, -1, linearDamping=100.0, lateralFriction=1, restitution=0.0)
		self.showcase.add(self.player.model)
		self.collision_objects[str(self.player.colId)] = self.player

		#UI showcase and camera
		self.UIshowcase = pyxie.showcase("UIcase##" + str(random.randrange(1000)))
		self.UIcam = pyxie.camera('UIcamera##' + str(random.randrange(1000)))
		self.UIcam.orthographicProjection = True
		self.UIcam.position = vmath.vec3(0.0, 0, 100)
		self.UIcam.target = vmath.vec3(0,0,0)
		self.UI_manager = UIManager()

		#Create button
		pos = [140,220,1]
		scale = [50, 50]
		self.powerUpButton = PowerButton(pos, scale, 'asset/power_up_button', self.UIshowcase, self.UIcam, self.UI_manager)

		#Create button
		pos = [-120,220,1]
		scale = [100, 30]
		self.replayButton = ReplayButton(pos, scale, 'asset/reset_button', self.UIshowcase, self.UIcam, self.UI_manager)

		# Create map
		# self.level = MapLevel('mapfiles/map.json', self.showcase, self.collision_objects)

		# Create cannon
		pos = vmath.vec3(0,-11,0.5)
		scale = vmath.vec3(1,1,1)
		rotation = vmath.quat([ 0, 0.7071068, 0.7071068, 0 ])
		self.cannon = Cannon(pos, scale, rotation, 'asset/Betakkuma/Canon_object', self.showcase)

		# Create final scene
		self.finalScene = FinalScene()

		#DEBUG ON GUI MODE
		self.cameraDistance = 10
		self.cameraYaw = 0
		self.cameraPitch = -35
		
	
	def Update(self):
		if self.state == "Reset":
			self.ResetScene()
			return

		if self.state == "Initing":
			self.initDt += 1
			if self.initDt > 10:
				self.initDt = 0
				self.state = "Playing"
			return

		if self.totalstepdt > self.stepdt:
			p.stepSimulation()
		while self.totalstepdt > self.stepdt:
			self.totalstepdt -= self.stepdt
	
		dt = pyxie.getElapsedTime()
		self.totalstepdt += dt
		
		touch = pyxie.singleTouch()
		if not touch or not touch['is_holded']:
			self.UI_manager.isTouchOnUI = False

		#Cannon
		# quat = self.cannon.model.rotation
		# dQuat = vmath.quat_rotationZ(0.1)
		# rotQuat = vmath.mul(quat, dQuat)
		# self.cannon.model.rotation = rotQuat

		#UI update
		self.powerUpButton.Update(touch)
		self.replayButton.Update(touch)

		#Other objects update
		self.player.update(dt, touch, self.collision_objects, self.UI_manager)
		
		self.cam.shoot(self.showcase)
		self.UIcam.shoot(self.UIshowcase, clearColor=False)
		# self.level.update(touch, self.player)

		playerPos, orn = p.getBasePositionAndOrientation(self.player.colId)

		cameraTargetPosition = playerPos
		# p.resetDebugVisualizerCamera(self.cameraDistance, self.cameraYaw, self.cameraPitch, cameraTargetPosition)

	def OnExit(self):
		p.disconnect()
		del self.cam
		del self.showcase
		del self.UIcam
		del self.UIshowcase
		self.__dict__.clear()

	def ResetScene(self):
		self.OnExit()
		self.Init()
	
	def SetState(self, state):
		self.state = state