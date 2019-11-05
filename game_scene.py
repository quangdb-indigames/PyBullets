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
from speed_button import SpeedButton
from pause_button import PauseButton
from reset_data_button import ResetDataButton
import imgui
from pyxie.apputil.imguirenderer import ImgiPyxieRenderer
from destroy_bar import DestroyBar
from progress_bar import ProgressBar
from end_stage_canvas import EndStageCanvas
from player import Player
from mapLevel import MapLevel
from skybox import Skybox
import json
STATE_RESET = "STATE_RESET"
STATE_RETRY = "STATE_RETRY"
STATE_INITING = "STATE_INITING"
STATE_PLAYING = "STATE_PLAYING"
STATE_PAUSE = "STATE_PAUSE"
class GameScene:
	def __init__(self):
		self.Init()

	def Init(self):
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

		#Setting IMGUI
		if not hasattr(self, "impl"):
			self.impl = ImgiPyxieRenderer()
			self.impl.io.font_global_scale = 1.0

		self.averageFPS = 60
		self.listFPS = list()
		self.listRecentAverageFPS = list()
		self.updateFpsRate = 10
		self.currentFpsCount = 0
		self.log = list()
		
		self.stepdt = 1 / FPS
		self.totalstepdt = 0
		p.setRealTimeSimulation(0)
		ddt = 1.0 / FPS

		#Init state
		self.state = STATE_INITING
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

		#SKYBOX REGION
		self.skyboxCamera = pyxie.camera('skyboxCam###' + str(random.randrange(1000)))
		self.skyboxCase = pyxie.showcase("skyboxCase##" + str(random.randrange(1000)))
		self.skyboxCamera.farPlane = 2000
		self.skybox = Skybox('asset/skybox/sphere_skybox_object', self.cam, self.skyboxCamera, self.skyboxCase)

		scale = vmath.vec3(10, 10, 10)
		position = vmath.vec3(0.0, -10.0, 0.75)
		player_col_scale = [0.1, 0.1, 1]
		player_col_local_pos = [0.0, 0.0, 1.1]
		self.player = Player(position, scale, [ 0, 0.7071068, 0.7071068, 0 ], 'asset/betakkuma/betakkuma', self.cam, player_col_scale, player_col_local_pos, True)
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

		# #Create button
		# pos = [140,220,1]
		# scale = [50, 50]
		# self.powerUpButton = PowerButton(pos, scale, 'asset/power_up_button', self.UIshowcase, self.UIcam, self.UI_manager)

		# Create speed button
		pos = [120, 70, 1]
		scale = [20, 300]
		tickScale = [20, 10]
		self.speedButton = SpeedButton(pos, scale, tickScale, 'asset/bar right 01', 'asset/bar right 02', self.UIshowcase, 5.0)

		#Create replay button
		pos = [-100,220,1]
		scale = [50, 30]
		self.replayButton = ReplayButton(pos, scale, 'asset/button_replay', self.UIshowcase, self.UIcam, self.UI_manager)

		#Create reset data button
		pos = [-100,180,1]
		scale = [40, 40]
		self.resetDataButton = ResetDataButton(pos, scale, 'asset/reset_data_button', self.UIshowcase, self.UIcam, self.UI_manager)

		# Create pause button
		pos = [120,220,1]
		scale = [20, 26]
		self.pauseButton = PauseButton(pos, scale, 'asset/button_pause', self.UIshowcase, self.UIcam, self.UI_manager)

		# Create progress bar
		progress_bar = ProgressBar([15, 220, 1], [150, 17], [142, 7], [23, 19], 'asset/progress_bar_background_bar', 'asset/progress_bar_slider_bar', 'asset/progress_bar_slider_normal', 'asset/progress_bar_slider_alert', self.UIshowcase)

		# Create destroy bar
		destroy_bar = DestroyBar([15, 220, 1], [150, 17], [142, 7], [1, 8.5], 'asset/progress_bar_background_bar', 'asset/destroy_bar_slider_bar', 'asset/destroy_bar_tick', self.UIshowcase)

		# Create end stage canvas
		end_stage_canvas = EndStageCanvas(
			[0,-25,0], [185, 165], [120, 80], 
			[38, 36], [100, 30], 
			'asset/end_stage_board', 'asset/end_stage_clear_stage_text', 'asset/end_stage_star_white', 'asset/end_stage_star_yellow', 'asset/end_stage_next_button', 'asset/end_stage_retry_button',
			self.UIshowcase, self.UIcam, self.UI_manager
		)

		# Create map
		self.level = MapLevel('mapfiles/map.json', self.showcase, self.collision_objects, progress_bar, destroy_bar, end_stage_canvas)
		# self.level.CreateACell("mapfiles/final_cell.json", [0,0,0])

		# Create cannon
		pos = vmath.vec3(0,-11,0.5)
		scale = vmath.vec3(1,1,1)
		rotation = vmath.quat([ 0, 0.7071068, 0.7071068, 0 ])
		self.cannon = Cannon(pos, scale, rotation, 'asset/betakkuma/Canon_object', self.showcase)

		# Create final scene
		# self.finalScene = FinalScene(self.showcase)

		#DEBUG ON GUI MODE
		self.cameraDistance = 10
		self.cameraYaw = 0
		self.cameraPitch = -35
		
	def DisplayFPS(self, elapsedTime):
		imgui.set_next_window_size(70, 50, imgui.ONCE) # 60, 100
		imgui.set_next_window_position(120, 450, imgui.ONCE) # 0, 15
		fps = round(1/elapsedTime)
		imgui.begin("", flags=imgui.WINDOW_NO_COLLAPSE|imgui.WINDOW_NO_TITLE_BAR|imgui.WINDOW_NO_SCROLLBAR|imgui.WINDOW_NO_RESIZE|imgui.WINDOW_ALWAYS_AUTO_RESIZE)
		imgui.text(str(self.averageFPS))
		imgui.end()
	
	def DisplayLog(self):
		imgui.set_next_window_size(70, 50) # 60, 100
		imgui.set_next_window_position(10, 50) # 0, 15
		imgui.begin("Log", flags=imgui.WINDOW_NO_COLLAPSE)
		for log in self.log:
			imgui.text(log)
		imgui.end()

	def CheckPhysicStep(self):
		if len(self.listRecentAverageFPS) > 5:
			average = sum(self.listRecentAverageFPS) / len(self.listRecentAverageFPS)
			if average <= 30:
				self.stepdt = 1/ 120
			elif average <= 40:
				self.stepdt = 1/100
			elif average <= 50:
				self.stepdt = 1/80
			else:
				self.stepdt = 1/60
			self.listRecentAverageFPS.clear()
	
	def UpdateFPS(self):
		avg_FPS = sum(self.listFPS) / len(self.listFPS)
		self.averageFPS = round(avg_FPS)
		self.listFPS.clear()
			
	def Update(self):
		touch = pyxie.singleTouch()
		self.impl.process_inputs()
		imgui.new_frame()

		if self.state == STATE_RETRY:
			self.ResetScene(2)
			return

		if self.state == STATE_RESET:
			self.ResetScene()
			return

		if self.state == STATE_INITING:
			self.initDt += 1
			if self.initDt > 10:
				self.initDt = 0
				self.state = STATE_PLAYING
			return
			
		if not touch or not touch['is_holded']:
			self.UI_manager.isTouchOnUI = False
		self.pauseButton.Update(touch)
		if self.state == STATE_PAUSE:
			return

		if self.totalstepdt > self.stepdt:
			p.stepSimulation()
		while self.totalstepdt > self.stepdt:
			self.totalstepdt -= self.stepdt
	
		dt = pyxie.getElapsedTime()
		self.currentFpsCount += 1
		self.listFPS.append(1/dt)
		if self.currentFpsCount >= self.updateFpsRate:
			self.currentFpsCount = 0
			self.UpdateFPS()
			self.listRecentAverageFPS.append(self.averageFPS)
			self.CheckPhysicStep()


		self.totalstepdt += dt
		self.DisplayFPS(dt)
		# self.DisplayLog()
		
		#Cannon
		# quat = self.cannon.model.rotation
		# dQuat = vmath.quat_rotationZ(0.1)
		# rotQuat = vmath.mul(quat, dQuat)
		# self.cannon.model.rotation = rotQuat

		#UI update
		# self.powerUpButton.Update(touch)
		self.speedButton.Update()
		self.replayButton.Update(touch)
		self.resetDataButton.Update(touch)
		self.skybox.Update()
		

		#Other objects update
		self.player.update(dt, touch, self.collision_objects, self.UI_manager)

		self.level.update(touch, self.player)

		playerPos, orn = p.getBasePositionAndOrientation(self.player.colId)
		# self.finalScene.Update()

		cameraTargetPosition = playerPos
		# p.resetDebugVisualizerCamera(self.cameraDistance, self.cameraYaw, self.cameraPitch, cameraTargetPosition)
	
	def Render(self):
		self.skyboxCamera.shoot(self.skyboxCase)
		self.cam.farPlane = 200
		self.cam.shoot(self.showcase, clearColor=False)
		self.UIcam.shoot(self.UIshowcase, clearColor=False)
		imgui.render()
		self.impl.render(imgui.get_draw_data(), False)



	def OnExit(self):
		p.disconnect()
		self.level.Destroy()
		del self.cam
		self.showcase.clear()
		del self.showcase
		del self.UIcam
		self.UIshowcase.clear()
		del self.UIshowcase		
		# self.__dict__.clear()

	def ResetScene(self, typeSave=1):
		if typeSave == 1:
			self.level.SaveResult()
		self.OnExit()
		self.Init()
	
	def SetState(self, state):
		self.state = state
	
	def HideUI(self):
		self.replayButton.Hide()
		self.resetDataButton.Hide()