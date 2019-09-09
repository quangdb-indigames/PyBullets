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
	imgui.set_next_window_size(300, 100)
	imgui.begin("Example: item groups")

	imgui.begin_group()
	imgui.text("First group (buttons):")
	imgui.button("Button A")
	imgui.button("Button B")
	imgui.end_group()

	imgui.same_line(spacing=50)

	imgui.begin_group()
	imgui.text("Second group (text and bullet texts):")
	imgui.bullet_text("Bullet A")
	imgui.bullet_text("Bullet B")
	imgui.end_group()

	imgui.end()

	# END TESTING REGION
	imgui.render()
	impl.render(imgui.get_draw_data())
	pyxie.swap()