import pybullet as p
import time
import pybullet_data
from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
import math
import random
class Cannon:
	def __init__(self, pos, scale, rotation, modelPath, showcase):
		self.model = pyxie.figure(modelPath)
		self.model.position = pos
		self.model.scale = scale
		self.model.rotation = rotation
		self.showcase = showcase
		self.showcase.add(self.model)