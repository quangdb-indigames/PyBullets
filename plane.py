import pybullet as p
import time
import pybullet_data
from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
import math
import random
from cube import Cube

class Plane():
    def __init__(self, root_position, texture_path, matrix_scale, unit_scale, showcase):
        self.root_position = root_position
        self.texture_path = texture_path
        self.matrix_scale = matrix_scale
        self.unit_scale = unit_scale
        self.showcase = showcase
        self.cube_list = []
        self.__initialize()
    
    def update(self, touch):
        if len(self.cube_list) > 0:
            for cube in self.cube_list:
                cube.update(touch)

    def __initialize(self):
        for i in range(0, self.matrix_scale):
            for j in range(0, self.matrix_scale):
                position = self.__getPositionAndScaleOfCube(i, j)
                scale = [self.unit_scale.x / 2, self.unit_scale.y / 2, self.unit_scale.z / 2]
                pos_v3 = vmath.vec3(position)
                cube = Cube(pos_v3, self.unit_scale, self.texture_path, scale, [0,0,0], True)
                cube.model.rotation = vmath.quat([ 0, 0, 0, 1 ])
                self.showcase.add(cube.model)
                self.cube_list.append(cube)
    
    def __getPositionAndScaleOfCube(self, i, j): 
        x_pos = self.root_position.x + i * self.unit_scale.x 
        y_pos = self.root_position.y + j * self.unit_scale.y
        z_pos = self.root_position.z
        position = [x_pos, y_pos, z_pos]
        return position