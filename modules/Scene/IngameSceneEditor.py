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
from pyquaternion import Quaternion

class IngameSceneEditor():
	def __init__(self):
		self.cam = pyxie.camera('ingame-editor-cam')
		self.cam.lockon = False
		self.cam.position = vmath.vec3(0.0, -3.0, 3)
		# self.cam.target = vmath.vec3(0.0, 0.0, 0.0)
		self.cam.farPlane = 100.0

		self.showcase = pyxie.showcase("ingame-editor-showcase")
		imgui.create_context()
		self.impl = ImgiPyxieRenderer()
		self.model = pyxie.figure("asset/plane_with_street")
		self.model.position = vmath.vec3(0,0,0)
		self.showcase.add(self.model)
		self.currentControlObject = None
	
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

#region Player setting
		imgui.begin_group()
		player_layer, visible = imgui.collapsing_header("Player", True)

		if player_layer:
			imgui.text("Create player")
		imgui.end_group()
#endregion

#region Camera setting
		self.cameraSetting()
#endregion
		imgui.end()

	def render(self):
		imgui.render()
		self.impl.render(imgui.get_draw_data())
		self.cam.shoot(self.showcase, clearColor=False)

	def cameraSetting(self):
		imgui.begin_group()
		camera_layer, visible = imgui.collapsing_header("Camera", True)

		if camera_layer:
			# Setting position
			position = self.cam.position.x, self.cam.position.y, self.cam.position.z
			changed, position = imgui.drag_float3(
				"position", *position, format="%.1f", change_speed = 0.05
			)
			self.cam.position = vmath.vec3(position)

			# Setting rotation
			euler = self.__fromQuaternionToEuler(self.cam.rotation)
			pos = [self.cam.position.x, self.cam.position.y, self.cam.position.z]
			changed, euler = imgui.drag_float3(
				"rotation", *euler, format="%.2f", change_speed = 0.02
			)
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
		# Roll (X), Pitch (Y), Yaw(Z)
		roll, pitch, yaw = math.radians(euler[0] % 360), math.radians(euler[1] % 360), math.radians(euler[2] % 360)
		cy = math.cos(yaw * 0.5)
		sy = math.sin(yaw * 0.5)
		cp = math.cos(pitch * 0.5)
		sp = math.sin(pitch * 0.5)
		cr = math.cos(roll * 0.5)
		sr = math.sin(roll * 0.5)

		q = list()
		
		qx = cy * cp * sr - sy * sp * cr		# x
		qy = sy * cp * sr + cy * sp * cr		# y
		qz = sy * cp * cr - cy * sp * sr		# z
		qw = cy * cp * cr + sy * sp * sr		# w
		q.append(qx)
		q.append(qy)
		q.append(qz)
		q.append(qw)

		return q
	
	def __fromQuaternionToEuler(self, q1):
		test = q1.x*q1.y + q1.z*q1.w
		if (test > 0.499):
			heading = 2 * math.atan2(q1.x,q1.w)
			attitude = math.pi/2
			bank = 0
			return

		if (test < -0.499):
			heading = -2 * math.atan2(q1.x,q1.w)
			attitude = - math.pi/2
			bank = 0
			return

		sqx = q1.x*q1.x;
		sqy = q1.y*q1.y;
		sqz = q1.z*q1.z;
		heading = math.atan2(2*q1.y*q1.w-2*q1.x*q1.z , 1 - 2*sqy - 2*sqz);
		attitude = math.asin(2*test);
		bank = math.atan2(2*q1.x*q1.w-2*q1.y*q1.z , 1 - 2*sqx - 2*sqz)

		return [math.degrees(bank), math.degrees(heading), math.degrees(attitude)]
#endregion
