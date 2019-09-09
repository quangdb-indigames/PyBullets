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
from modules.Scene.IngameSceneEditor import IngameSceneEditor
from modules.Scene.SceneManager import SceneManager

pyxie.window(True, DEF.SCREEN_WIDTH , DEF.SCREEN_HEIGHT)

ingameSceneEditorMode = IngameSceneEditor()
SceneManager.list_scene.append(ingameSceneEditorMode)

while(1):
	touch = pyxie.singleTouch()
	SceneManager.Singleton_GetCurrentScene().update(touch)
	SceneManager.Singleton_GetCurrentScene().render()

	pyxie.swap()