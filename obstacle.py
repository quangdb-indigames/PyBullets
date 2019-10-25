import pybullet as p
import time
import pybullet_data
from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
import math
import random
class Obstacle:
    def __init__(self, obj, move_speed, start_pos, end_pos):
        self.obj = obj
        self.move_speed = move_speed
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.currentTargetPos = self.end_pos
        self.reverseDistance = 1.0
    
    def Update(self):
        self.CheckDistance()
        self.MoveToTargetPos()

    def CheckDistance(self):
        pos, orn = p.getBasePositionAndOrientation(self.obj.colId)
        disVector = [self.currentTargetPos[0] - pos[0], self.currentTargetPos[1] - pos[1], self.currentTargetPos[2] - pos[2]]
        dis = vmath.length(vmath.vec3(disVector))
        if dis <= self.reverseDistance:
            self.ReverseTargetPosition()

    def ReverseTargetPosition(self):
        if self.currentTargetPos == self.end_pos:
            self.currentTargetPos = self.start_pos
        elif self.currentTargetPos == self.start_pos:
            self.currentTargetPos = self.end_pos
    
    def MoveToTargetPos(self):
        pos, orn = p.getBasePositionAndOrientation(self.obj.colId)
        linearVelocity, angularVelocity = linearVelocity, angularVelocity = p.getBaseVelocity(self.obj.colId)
        newVelocity = self.CalculateVelocity(pos)
        p.resetBaseVelocity(self.obj.colId, newVelocity, angularVelocity)


    def CalculateVelocity(self, pos):
        direction = [self.currentTargetPos[0] - pos[0], self.currentTargetPos[1] - pos[1], self.currentTargetPos[2] - pos[2]]
        normalizeDirection = vmath.normalize(vmath.vec3(direction))
        newVelocity = [normalizeDirection.x * self.move_speed, normalizeDirection.y * self.move_speed, normalizeDirection.z * self.move_speed]
        return newVelocity