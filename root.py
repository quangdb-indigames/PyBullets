import pybullet as p
import time
import pybullet_data
from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
import math
import random
from game_scene import GameScene
from scene_manager import SceneManager
import imgui

SCREEN_WIDTH = 520
SCREEN_HEIGHT = 900
pyxie.window(True, SCREEN_WIDTH , SCREEN_HEIGHT)
imgui.create_context()
gameScene = GameScene()

SceneManager.SetCurrentScene(gameScene)

while(1):
	
	SceneManager.GetCurrentScene().Update()
	SceneManager.GetCurrentScene().Render()
	pyxie.swap()
