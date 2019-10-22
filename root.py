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

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
pyxie.window(True, SCREEN_WIDTH , SCREEN_HEIGHT)

gameScene = GameScene()

SceneManager.SetCurrentScene(gameScene)

while(1):
	
	SceneManager.GetCurrentScene().Update()
	pyxie.swap()
