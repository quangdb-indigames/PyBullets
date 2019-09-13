from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
import math
from modules.Helper import helperFunction
from modules.Object.game_object import GameObject
from modules.Object.mesh import Mesh
from modules.Object.box_collider import BoxCollider
class Player(GameObject):
	def __init__(self, modelPath, name = "GameObject", position = [0.0,0.0,0.0], scale  = [1.0,1.0,1.0], rotation = [0.0,0.0,0.0]):
		super().__init__(name, position, scale, rotation)
		mesh = Mesh(self, modelPath)
		self.components.append(mesh)
		self.testAttr = 1
	
	def update(self, updateSelf = True):
		super().update(updateSelf)
	
	def addColider(self, colPath, showcase):
		col = BoxCollider(self, colPath, showcase)
		self.components.append(col)