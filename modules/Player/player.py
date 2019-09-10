import pybullet as p
import time
import pybullet_data
from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
import math
import random
class Player():
    def __init__(self, position, scale, modelPath, showcase, cam, base_rotate=[0,0,0,1]):
        self.position = position
        self.scale = scale
        self.modelPath = modelPath
        self.cam = cam
        self.base_rotate = base_rotate
        self.showcase = showcase
        
        # Setting up
        self.model = pyxie.figure(modelPath)
        self.model.position = vmath.vec3(self.position)
        self.model.scale = vmath.vec3(self.scale)
        self.model.rotation = vmath.quat(base_rotate)
        self.showcase.add(self.model)