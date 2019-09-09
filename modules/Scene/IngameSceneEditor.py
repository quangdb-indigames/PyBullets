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
		self.cam.lockon = True
		self.cam.position = vmath.vec3(0.0, -3.0, 3)
		self.cam.target = vmath.vec3(0.0, 0.0, 0.0)
		self.cam.farPlane = 100.0

		self.showcase = pyxie.showcase("ingame-editor-showcase")
		imgui.create_context()
		self.impl = ImgiPyxieRenderer()
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

#region New Test
	
#end region
		imgui.end()

	def render(self):
		imgui.render()
		self.impl.render(imgui.get_draw_data())

	def cameraSetting(self):
		imgui.begin_group()
		camera_layer, visible = imgui.collapsing_header("Camera", True)

		if camera_layer:
			# Setting position
			position = self.cam.position.x, self.cam.position.y, self.cam.position.z
			changed, position = imgui.drag_float3(
				"position", *position, format="%.1f"
			)
			self.cam.position = vmath.vec3(position)

			# Setting rotation
			quat =  self.cam.rotation.x, self.cam.rotation.y, self.cam.rotation.z, self.cam.rotation.w
			pos = [self.cam.position.x, self.cam.position.y, self.cam.position.z]
			changed, quat = imgui.drag_float4(
				"rotation", *quat, format="%.2f", change_speed = 0.02
			)
			self.cam.rotation = vmath.quat(vmath.normalize(quat))
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
#endregion
