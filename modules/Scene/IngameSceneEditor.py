import pybullet as p
import time
import pybullet_data
from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
import math
import random
import imgui
from pyxie.apputil.imguirenderer import ImgiPyxieRenderer
from modules.Helper import define as DEF
from modules.Player.player import Player
from pyquaternion import Quaternion

class IngameSceneEditor():
	def __init__(self):
		self.cam = pyxie.camera('ingame-editor-cam')
		self.cam.lockon = False
		self.cam.position = vmath.vec3(0.0, -3.0, 3)
		# self.cam.target = vmath.vec3(0.0, 0.0, 0.0)
		self.cam.farPlane = 100.0
		self.camPreviousAngle = [0,0,0]

		self.showcase = pyxie.showcase("ingame-editor-showcase")
		imgui.create_context()
		self.impl = ImgiPyxieRenderer()
		self.model = pyxie.figure("asset/plane_with_street")
		self.model.position = vmath.vec3(0,0,0)
		self.showcase.add(self.model)
		self.currentControlObject = None
		self.player = None
		self.playerPreviousAngle = [0,0,0]
	
	def update(self, touch):
		curX, curY, press = self.__processCursorInformation(touch)
		imgui.new_frame()
		io = imgui.get_io()
		io.font_global_scale = 0.5
		# IMGUI TESTING REGION
		imgui.begin("Level Editor")
		imgui.text("Screen size: w = {}, h = {} ".format(DEF.SCREEN_WIDTH, DEF.SCREEN_HEIGHT))
		imgui.text("Camera position: x = {}, y = {}, z = {}".format(self.cam.position.x, self.cam.position.y, self.cam.position.z))
		imgui.text("x={}:y={}:press={}".format(curX, curY, press))
		if self.currentControlObject is not None:
			imgui.text("Current control obj: ".format(self.currentControlObject))

#region Player setting
		self.playerSetting()
#endregion

#region Camera setting
		self.cameraSetting()
#endregion
		imgui.end()

	def render(self):
		imgui.render()
		self.impl.render(imgui.get_draw_data())
		self.cam.shoot(self.showcase, clearColor=False)
	
	def playerSetting(self):
		imgui.begin_group()
		player_layer, visible = imgui.collapsing_header("Player", True)
		if player_layer:
			if imgui.button("Create"):
				if self.player is not None:
					self.showcase.remove(self.player.model)
				self.player = Player([0,0,0], [1,1,1], "asset/Sapphiart", self.showcase, self.cam)
				self.currentControlObject = self.player
			
			if self.player is not None:
				# Setting position
				position = self.player.model.position.x, self.player.model.position.y, self.player.model.position.z
				changed, position = imgui.drag_float3(
					"position", *position, format="%.1f", change_speed = 0.05
				)
				self.player.model.position = vmath.vec3(position)

				# Setting rotation
				euler = self.playerPreviousAngle[0], self.playerPreviousAngle[1], self.playerPreviousAngle[2]
				pos = [self.player.model.position.x, self.player.model.position.y, self.player.model.position.z]
				changed, euler = imgui.drag_float3(
					"rotation", *euler, format="%.2f", change_speed = 0.5
				)
				
				if changed:
					self.playerPreviousAngle = euler
					quat = self.__fromEulerToQuaternion(euler)
					self.player.model.rotation = vmath.quat(quat)
					self.player.model.position = vmath.vec3(pos)
		imgui.end_group()
			

	def cameraSetting(self):
		imgui.begin_group()
		camera_layer, visible = imgui.collapsing_header("Camera", True)

		if camera_layer:
			self.currentControlObject = self.cam
			# Setting position
			position = self.cam.position.x, self.cam.position.y, self.cam.position.z
			changed, position = imgui.drag_float3(
				"position", *position, format="%.1f"
			)
			self.cam.position = vmath.vec3(position)

			# Setting rotation
			euler = self.camPreviousAngle[0], self.camPreviousAngle[1], self.camPreviousAngle[2]
			pos = [self.cam.position.x, self.cam.position.y, self.cam.position.z]
			changed, euler = imgui.drag_float3(
				"rotation", *euler, format="%.2f", change_speed = 0.5
			)
			if changed:
				self.camPreviousAngle = euler
				print(euler)
				quat = self.__fromEulerToQuaternion(euler)
				self.cam.rotation = vmath.quat(quat)
				self.cam.position = vmath.vec3(pos)
		imgui.end_group()

#region Helper function
	def __processCursorInformation(self, touch):
		w, h = pyxie.viewSize()
		curX = 0
		curY = 0
		press = 0
		touch = pyxie.singleTouch()
		if touch != None:
			curX = touch['cur_x'] + w // 2
			curY = -touch['cur_y'] + h // 2
			press = touch['is_holded'] | touch['is_moved']
		self.impl.process_inputs()
		return curX, curY, press
	
	def __fromEulerToQuaternion(self, euler):
		# XZY
		x, y, z = math.radians(euler[0] % 360), math.radians(euler[1] % 360), math.radians(euler[2] % 360)

		cz = math.cos(z * 0.5)
		sz = math.sin(z * 0.5)
		cy = math.cos(y * 0.5)
		sy = math.sin(y * 0.5)
		cx = math.cos(x * 0.5)
		sx = math.sin(x * 0.5)

		q = list()
		
		qx = sx * cy * cz - cx * sy * sz		# x
		qy = cx * cy * sz + sx * sy * cz		# y
		qz = cx * sy * cz - sx * cy * sz		# z
		qw = cx * cy * cz + sx * sy * sz		# w
		q.append(qx)
		q.append(qy)
		q.append(qz)
		q.append(qw)
		return q
	
	# def __fromQuaternionToEuler(self, q1, previousAngle):
	# 	# Heading = rotation about y axis
	# 	# Attitude = rotation about z axis
	# 	# Bank = rotation about x axis
	# 	test = q1.x*q1.y + q1.z*q1.w
	# 	k_epsilon = 0.000001
	# 	if (test > 0.4995):
	# 		heading = 2 * math.atan2(q1.x,q1.w)
	# 		attitude = math.pi/2
	# 		bank = 0
	# 		return [math.degrees(bank), math.degrees(heading), math.degrees(attitude)]

	# 	if (test < -0.4995):
	# 		heading = -2 * math.atan2(q1.x,q1.w)
	# 		attitude = - math.pi/2
	# 		bank = 0
	# 		return [math.degrees(bank), math.degrees(heading), math.degrees(attitude)]

	# 	sqx = q1.x*q1.x;
	# 	sqy = q1.y*q1.y;
	# 	sqz = q1.z*q1.z;
	# 	heading = math.atan2(2*q1.y*q1.w-2*q1.x*q1.z , 1 - 2*sqy - 2*sqz);
	# 	attitude = math.asin(2*test);
	# 	bank = math.atan2(2*q1.x*q1.w-2*q1.y*q1.z , 1 - 2*sqx - 2*sqz)

	# 	euler_x = math.degrees(bank) % 360
	# 	euler_y =  math.degrees(heading) % 360
	# 	euler_z = math.degrees(attitude) % 360
		
	# 	if abs(euler_x - previousAngle[0]) < k_epsilon:
	# 		euler_x = previousAngle[0]
	# 	if abs(euler_y - previousAngle[1]) < k_epsilon:
	# 		euler_y = previousAngle[1]
	# 	if abs(euler_z - previousAngle[2]) < k_epsilon:
	# 		euler_z = previousAngle[2]

	# 	return [euler_x,euler_y, euler_z]
#endregion
