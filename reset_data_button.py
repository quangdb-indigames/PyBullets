from pyxie.apputil import graphicsHelper
import pyxie
import pyvmath as vmath
import json
import os
from scene_manager import SceneManager
class ResetDataButton():
	def __init__(self, pos, scale, filePath, showcase, camera, ui_manager):
		self.position = pos
		self.scale = scale
		self.filePath = filePath
		self.camera = camera
		self.showcase = showcase
		self.model = graphicsHelper.createSprite(self.scale[0], self.scale[1], self.filePath)
		self.model.position = vmath.vec3(self.position)
		self.ui_manager = ui_manager

		self.tapped = False

		self.showcase.add(self.model)
	
	def Update(self, touch):
		self.CheckOnClick(touch)
	
	def CheckOnClick(self, touch):
		if touch:
			if touch['is_holded']:			
				if self.CheckInside(touch) and not self.tapped:
					self.tapped = True
					self.ui_manager.isTouchOnUI = True
					self.OnClickExcute()
			else:
				self.tapped = False
		else:
			self.tapped = False
	
	def CheckInside(self, touch):
		direction = self.ConvertScreenToWorld(touch['cur_x'], touch['cur_y'], 0, self.camera)
		if direction.x <= self.model.position.x + self.scale[0] / 2 and direction.x >= self.model.position.x - self.scale[0] / 2 \
			and direction.y <= self.model.position.y + self.scale[1] / 2 and direction.y >= self.model.position.y - self.scale[1] / 2:
			return True
		return False
	
	def OnClickExcute(self):
		if os.path.exists("TestVoxel/activatedBodies.pickle"):
			os.remove("TestVoxel/activatedBodies.pickle")

	
	def ConvertScreenToWorld(self, scrx, scry, worldz, cam, w=None, h=None):
		invproj = vmath.inverse(cam.projectionMatrix)
		invview = cam.viewInverseMatrix
		if not w or not h:
			w, h = pyxie.viewSize()
		x = scrx / w * 2
		y = scry / h * 2

		pos = vmath.vec4(x, y, 0.0, 1.0)
		npos = invproj * pos
		npos = invview * npos
		npos.z /= npos.w
		npos.x /= npos.w
		npos.y /= npos.w
		npos.w = 1.0
		pos = vmath.vec4(x, y, 1.0, 1.0)
		fpos = invproj * pos
		fpos = invview * fpos
		fpos.z /= fpos.w
		fpos.x /= fpos.w
		fpos.y /= fpos.w
		fpos.w = 1.0

		dir = vmath.normalize(fpos - npos)
		return npos + (dir * (npos.z - worldz))