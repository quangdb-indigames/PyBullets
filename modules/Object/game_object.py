from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
class GameObject():
    def __init__(self, name = "GameObject", position = [0,0,0], scale  = [1,1,1], rotation = [0,0,0]):
        self.parent = None
        self.child = []
        
        self.name = name
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.components = []
     
    def __repr__(self):
        print("Class: ", self.__class__, ", Object's name: ", self.name)
