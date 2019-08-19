import pybullet as p
import time
import pybullet_data
from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
import math
import random

def getRayFromTo(mouseX, mouseY):
    
  width, height, viewMat, projMat, cameraUp, camForward, horizon, vertical, _, _, dist, camTarget = p.getDebugVisualizerCamera(
  )
  camPos = [
      camTarget[0] - dist * camForward[0], camTarget[1] - dist * camForward[1],
      camTarget[2] - dist * camForward[2]
  ]
  farPlane = 10000
  rayForward = [(camTarget[0] - camPos[0]), (camTarget[1] - camPos[1]), (camTarget[2] - camPos[2])]
  invLen = farPlane * 1. / (math.sqrt(rayForward[0] * rayForward[0] + rayForward[1] *
                                      rayForward[1] + rayForward[2] * rayForward[2]))
  rayForward = [invLen * rayForward[0], invLen * rayForward[1], invLen * rayForward[2]]
  rayFrom = camPos
  oneOverWidth = float(1) / float(width)
  oneOverHeight = float(1) / float(height)
  dHor = [horizon[0] * oneOverWidth, horizon[1] * oneOverWidth, horizon[2] * oneOverWidth]
  dVer = [vertical[0] * oneOverHeight, vertical[1] * oneOverHeight, vertical[2] * oneOverHeight]
  rayToCenter = [
      rayFrom[0] + rayForward[0], rayFrom[1] + rayForward[1], rayFrom[2] + rayForward[2]
  ]
  rayTo = [
      rayToCenter[0] - 0.5 * horizon[0] + 0.5 * vertical[0] + float(mouseX) * dHor[0] -
      float(mouseY) * dVer[0], rayToCenter[1] - 0.5 * horizon[1] + 0.5 * vertical[1] +
      float(mouseX) * dHor[1] - float(mouseY) * dVer[1], rayToCenter[2] - 0.5 * horizon[2] +
      0.5 * vertical[2] + float(mouseX) * dHor[2] - float(mouseY) * dVer[2]
  ]
  return rayFrom, rayTo


SCREEN_WIDTH = 480
SCREEN_HEIGHT = 1000
physicsClient = p.connect(p.GUI)

boxHalfLength = 0.5
boxHalfWidth = 0.5
boxHalfHeight = 0.5
segmentLength = 5

colBoxId = p.createCollisionShape(p.GEOM_BOX,
								  halfExtents=[boxHalfLength, boxHalfWidth, boxHalfHeight])

p.createMultiBody(baseMass = 10, baseCollisionShapeIndex = colBoxId, basePosition= [0.0, 2.0, 1.0]);
p.changeVisualShape(colBoxId, -1, rgbaColor=[0.5, 0.1, 0.7, 1])

p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -10)
planeId = p.loadURDF("plane.urdf")
# cubeStartPos = [0, 0, 1]
# cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
# boxId = p.loadURDF("r2d2.urdf", cubeStartPos, cubeStartOrientation)
while(1):
	mouseEvents = p.getMouseEvents()
	for e in mouseEvents:
		if ((e[0] == 2) and (e[3] == 0) and (e[4] & p.KEY_WAS_TRIGGERED)):
			mouseX = e[1]
			mouseY = e[2]
			rayFrom, rayTo = getRayFromTo(mouseX, mouseY)
			rayInfo = p.rayTest(rayFrom, rayTo)
			for l in range(len(rayInfo)):
				hit = rayInfo[l]
				objectUid = hit[0]
				if(objectUid >= 0):
					p.changeVisualShape(objectUid, -1, rgbaColor=[random.random(), random.random(), random.random(), 1])
					pos, orn = p.getBasePositionAndOrientation(objectUid)
					p.applyExternalForce(objectUid, -1, forceObj=[0, 0, 10.0], posObj=pos, flags=p.WORLD_FRAME)
	p.stepSimulation()
	time.sleep(1. / 240.)


