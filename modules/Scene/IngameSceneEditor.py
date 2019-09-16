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
from modules.Helper import helperFunction as HELPER
from modules.Object.game_object import GameObject
from modules.Player.player import Player
from modules.Object.mesh import Mesh
from os import walk

class IngameSceneEditor():
	def __init__(self):
		self.currentSceneObjects = list()	
		
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
		self.openInspector = False

		f = []
		for (dirpath, dirnames, filenames) in walk("modules"):
			f.extend(dirnames)
			f.extend(filenames)
			break

	def update(self, touch):
		curX, curY, press = self.__processCursorInformation(touch)
		imgui.new_frame()
		io = imgui.get_io()
		io.font_global_scale = 0.4

#region LEVEL EDITOR WINDOW
		self.style = imgui.get_style()
		self.style.scrollbar_size = 3

		imgui.begin("Level Editor")
		imgui.text("Screen size: w = {}, h = {} ".format(DEF.SCREEN_WIDTH, DEF.SCREEN_HEIGHT))
		if self.currentControlObject is not None:
			imgui.text("Current control obj: {}".format(self.currentControlObject))
		imgui.text("Camera position: x = {}, y = {}, z = {}".format(self.cam.position.x, self.cam.position.y, self.cam.position.z))
		imgui.text("x={}:y={}:press={}".format(curX, curY, press))		

#region Player setting
		self.playerSetting()
#endregion

#region Camera setting
		self.cameraSetting()
#endregion

#region Testing
		imgui.begin_group()
		current = 1
		clicked, current = imgui.combo(
			"combo", current, ["first", "second", "third"]
		)
		imgui.end_group()
#endregion
		imgui.end()
#endregion

#region HIERACHY
		imgui.set_next_window_size(100, 150)
		imgui.begin("Hierachy")
		for obj in self.currentSceneObjects:
			self.displayGameObjectOnHierarchy(imgui, obj)
		imgui.end()

		if self.currentControlObject != None and isinstance(self.currentControlObject, GameObject):
			self.displayObjectInspector(self.currentControlObject, imgui)
#endregion

#region TEST WINDOW
		# imgui.show_test_window()
#endregion

	def render(self):
		imgui.render()
		self.impl.render(imgui.get_draw_data())
		self.cam.shoot(self.showcase, clearColor=False)

#region INSPECTOR
	def displayObjectInspector(self, obj, imgui):
		imgui.set_next_window_size(150, 100)
		imgui.set_next_window_position(5, 160)
		expanded, opened = imgui.begin("Inspector", True)
		if opened:
			imgui.begin_group()
			imgui.bullet_text(obj.name)

			transform_layer, visible = imgui.collapsing_header("Transform", True)
			if transform_layer:
				HELPER.displayGameObjectTransformSetting(obj, imgui)
			imgui.end_group()

			for component in obj.components:
				HELPER.displayComponentSetting(imgui, component, obj)
		else:
			self.openInspector = False
		imgui.end()
#endregion

#region HIERARCHY implement

	def displayGameObjectOnHierarchy(self, imgui, obj):
		if len(obj.childs) <= 0:
			imgui.indent(5)
			if imgui.selectable(obj.name)[1]:
				self.currentControlObject = obj
			imgui.unindent(5)
		elif len(obj.childs) > 0:
			imgui.unindent(5)
			object_layer = imgui.tree_node(obj.name, flags= imgui.TREE_NODE_OPEN_ON_ARROW)
			clicked = imgui.is_item_clicked()
			if clicked:
				self.currentControlObject = obj
			
			if object_layer:			
				for childObj in obj.childs:
					self.displayGameObjectOnHierarchy(imgui, childObj)
				imgui.tree_pop()
#endregion
	
#region Player Setting implement
	def playerSetting(self):
		imgui.begin_group()
		player_layer, visible = imgui.collapsing_header("Player", True)
		if player_layer:
			player = HELPER.getObjectOfType(Player, self.currentSceneObjects)
			self.currentControlObject = player
			if imgui.button("Create"):
				print(imgui.core.get_style())
				player = self.createNewPlayer()
				self.currentControlObject = player
		imgui.end_group()
	
	def createNewPlayer(self):
		player = HELPER.getObjectOfType(Player, self.currentSceneObjects)
		try:
			self.currentSceneObjects.remove(player)
			playerMesh = player.getComponent(Mesh)
			self.showcase.remove(playerMesh.mesh)
		except:
			pass

		player = Player("asset/cube_02", "Sapphi-chan", rotation=[45.0, 90.0, 0.0])
		self.currentSceneObjects.append(player)
		playerMesh = player.getComponent(Mesh)
		self.showcase.add(playerMesh.mesh)

		# player.addColider("asset/cube_02", self.showcase)
		childObj = Player("asset/cube_02", "ChildObj", [1.0, 1.0, 0.0])
		childMesh = childObj.getComponent(Mesh)
		self.showcase.add(childMesh.mesh)
		childObj.setParent(player)

		# Testing
		childObj2 = Player("asset/cube_02", "ChildObj_2")
		childObj2.setParent(player)

		child_depth2 = Player("asset/cube_02", "Child_depth2_01")
		child_depth2.setParent(childObj2)
		child_depth2 = Player("asset/cube_02", "Child_depth2_02")
		child_depth2.setParent(childObj2)
		return player


#endregion			

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
				quat = HELPER.fromEulerToQuaternion(euler)
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
	
	def __settingWindowStyle(self):
		pass
	
#endregion
