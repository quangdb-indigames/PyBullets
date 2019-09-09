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

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
pyxie.window(True, SCREEN_WIDTH , SCREEN_HEIGHT)

cam = pyxie.camera('maincam')
cam.lockon = True
cam.position = vmath.vec3(0.0, -3.0, 3)
cam.target = vmath.vec3(0.0, 0.0, 0.0)
cam.farPlane = 100.0

showcase = pyxie.showcase("case01")
imgui.create_context()
impl = ImgiPyxieRenderer()
while(1):
	w, h = pyxie.viewSize()
	curX = 0
	curY = 0
	press = 0
	touch = pyxie.singleTouch()
	if touch != None:
		curX = touch['cur_x'] + w // 2
		curY = -touch['cur_y'] + h // 2
		press = touch['is_holded'] | touch['is_moved']
	impl.process_inputs()
	imgui.new_frame()

	io = imgui.get_io()
	io.font_global_scale = 0.5

	# IMGUI TESTING REGION
	imgui.begin("Level Editor")
	imgui.text("Screen size: w = {}, h = {} ".format(SCREEN_WIDTH, SCREEN_HEIGHT))
	imgui.text("Camera position: x = {}, y = {}, z = {}".format(cam.position.x, cam.position.y, cam.position.z))
	imgui.text("x={}:y={}:press={}".format(curX, curY, press))

#region Player setting
	imgui.begin_group()
	player_layer, visible = imgui.collapsing_header("Player", True)

	if player_layer:
		imgui.text("Create player")
	imgui.end_group()
#endregion

#region Camera setting
	imgui.begin_group()
	camera_layer, visible = imgui.collapsing_header("Camera", True)

	if camera_layer:
		imgui.text("Camera position: x = {}, y = {}, z = {}".format(cam.position.x, cam.position.y, cam.position.z))
		posX = cam.position.x
		posY = cam.position.y
		posZ = cam.position.z
		changed, posX = imgui.drag_float(
			"x", cam.position.x, format="%.1f"
		)
		changed, posY = imgui.drag_float(
			"y", cam.position.y, format="%.1f"
		)
		changed, posZ = imgui.drag_float(
			"z", cam.position.z, format="%.1f"
		)
		cam.position = vmath.vec3(posX, posY, posZ)
	imgui.end_group()
#endregion
	imgui.end()

	# END TESTING REGION
	imgui.render()
	impl.render(imgui.get_draw_data())
	pyxie.swap()