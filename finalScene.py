import pyxie
from pyxie import devtool
import pickle
import pyvmath as vmath
import pybullet as p
import os
import glob

INIT_STATE = "INIT_STATE"
ACTIVE_STATE = "ACTIVE_STATE"
class FinalScene:
	def __init__(self, showcase):
		# Variable
		self.state = INIT_STATE
		self.showcase = showcase
		self.sizeMulti = 100
		self.activatedBodies = list()
		self.removedBodies = list()
		self.firstTimeActive = True

		#Init process
		self.VoxelModelProcess()

		#Load handled box data
		self.LoadNewBoxData()

	def ToActivateState(self):
		#When to state
		self.ConstructPybulletProcess()

		#Activate process
		self.state = ACTIVE_STATE
		self.PyxieDisplayProcess()

		# Handle removed body
		self.HandleRemovedBodies()

	def Update(self):
		if self.state == INIT_STATE:
			return
		self.SimulateProcess()
		
	def PyxieDisplayProcess(self):
		self.model = pyxie.figure("TestVoxel/Lion_Enemy")
		# self.model.scale = vmath.vec3(self.sizeMulti, self.sizeMulti, self.sizeMulti)
		self.showcase.add(self.model)
	
	def SimulateProcess(self):
		index = 1
		for bd in self.bodies:
			if not bd:
				index += 1
				continue

			if not self.firstTimeActive and bd not in self.activatedBodies:
				index += 1
				continue
			pos, rot = p.getBasePositionAndOrientation(bd)
			self.model.setJoint(index, position=vmath.vec3(pos), rotation=vmath.quat(rot), scale=vmath.vec3(self.sizeMulti, self.sizeMulti, self.sizeMulti ))
			index += 1			
		
		if self.firstTimeActive:
			self.firstTimeActive = False

	def VoxelModelProcess(self):
		# ------------------------------------------------------------
		# --pre process

		FILENAME = "TestVoxel/Lion_Voxel_340_04.dae"
		BOXINFOR_PATH = "TestVoxel/boxinfo.pickle"
		CONSTRUCT_BOXDATA_PATH = "TestVoxel/newConstructBoxData.pickle"

		# if os.path.exists("TestVoxel/boxinfo.pickle"):
		# 	os.remove("TestVoxel/boxinfo.pickle")

		if not os.path.exists(BOXINFOR_PATH) or not os.path.exists(CONSTRUCT_BOXDATA_PATH):
			print("Come here")
			# if True:

			efig = pyxie.editableFigure("efig")
			devtool.loadCollada(FILENAME, efig)

			boxinfo = []
			for i in range(efig.numMeshes):
				aabb = vmath.aabb()
				inverts = efig.getVertexElements(i, pyxie.ATTRIBUTE_ID_POSITION)
				for pos in inverts:
					aabb.insert(pos)
				outverts = []
				for pos in inverts:
					outverts.append(pos - aabb.center)
				efig.setVertexElements(i, pyxie.ATTRIBUTE_ID_POSITION, outverts)
				efig.setJoint(i, position=aabb.center)

				min, max = efig.getMeshAABB(i)
				pos, rot, _ = efig.getJoint(i)
				data = (
					(pos.x, pos.y, pos.z),
					(rot.x, rot.y, rot.z, rot.w),
					(min.x, min.y, min.z),
					(max.x, max.z, max.z),
				)
				boxinfo.append(data)
			newBoxData = self.HandleBoxData(boxinfo)
			
			newConstructBoxData = dict()
			newConstructBoxData.update(
				{
					"size": self.size,
					"center": self.center,
					"newBoxData": newBoxData
				}
			)

			src = efig.getTextureSource()
			for tex in src:
				texfilename = os.path.basename(tex['path'])
				name, _ = os.path.splitext(texfilename)
				newtex = tex.copy()
				newtex['path'] = "TestVoxel/" +  name
				print("New text path: ", newtex['path'])
				efig.replaceTextureSource(tex, newtex)
				filepath = glob.glob('**/'+texfilename, recursive=True)
				print("File path: ", filepath)
				if len(filepath) is not 0:
					devtool.convertTextureToPlatform(filepath[0], os.path.join(".", "TestVoxel\\" + name), pyxie.TARGET_PLATFORM_PC, tex['normal'], tex['wrap'])
					print("Path joining: ", os.path.join(".", name))

			with open(BOXINFOR_PATH, "wb") as f:
				pickle.dump(boxinfo, f)
			with open(CONSTRUCT_BOXDATA_PATH, "wb") as f:
				pickle.dump(newConstructBoxData, f)

			efig.mergeMesh()
			efig.saveFigure("TestVoxel/Lion_Enemy")
		# ------------------------------------------------------------

	def LoadNewBoxData(self):
		with open("TestVoxel/newConstructBoxData.pickle", "rb") as f:
			newConstructBoxData = pickle.load(f)
		
		self.size = newConstructBoxData['size']
		self.center = newConstructBoxData['center']
		self.newBoxData = newConstructBoxData['newBoxData']

	def HandleBoxData(self, boxData):
		# Size 
		self.size = boxData[0][3][0] - boxData[0][2][0]

		# Min x
		minX = boxData[0][0][0]
		# Max x
		maxX = boxData[0][0][0]
		# Min y
		minY = boxData[0][0][1]
		# Max y
		maxY = boxData[0][0][1]
		# Min z
		minZ = boxData[0][0][2]
		# Max z
		maxZ = boxData[0][0][2]
		for point in boxData:
			if point[0][0] < minX:
				minX = point[0][0]
			if point[0][1] < minY:
				minY = point[0][1]
			if point[0][2] < minZ:
				minZ = point[0][2]

			if point[0][0] > maxX:
				maxX = point[0][0]
			if point[0][1] > maxY:
				maxY = point[0][1]
			if point[0][2] > maxZ:
				maxZ = point[0][2]
		
		root =  [(maxX + minX) / 2, (maxY + minY) / 2, (maxZ + minZ) / 2]

		matrixList = self.Matrilization(root, self.size, boxData)
		# Handle pos and scale
		translate = [0, 1500, 7.0]
		self.size *= self.sizeMulti
		newRoot = [root[0] + translate[0], root[1] + translate[1], root[2] + translate[2]]
		self.center = newRoot
		newBoxData = self.CalculatePositionWithNewSize(newRoot, matrixList, self.size)
		return newBoxData

	def CalculatePositionWithNewSize(self, root, matrixList, newSize):
		newBoxData = list()
		for point in matrixList:
			posX = root[0] + point[0] * newSize
			posY = root[1] + point[1] * newSize
			posZ = root[2] + point[2] * newSize
			newBoxData.append([posX, posY, posZ])
		return newBoxData

	def Matrilization(self, root, size, boxData):
		matrixList = list()
		for point in boxData:
			pos = point[0]
			i = (pos[0] - root[0]) / size
			j = (pos[1] - root[1]) / size
			k = (pos[2] - root[2]) / size
			matrixList.append([i, j, k])
		return matrixList
	
	def ConstructPybulletProcess(self):
		boxinfo = []
		with open("TestVoxel/boxinfo.pickle", "rb") as f:
			boxinfo = pickle.load(f)

		self.bodies = []

		box1 = boxinfo[0]
		SCALE = 0.98
		shape = p.createCollisionShape(
			p.GEOM_BOX, halfExtents=[self.size / 2 * SCALE, self.size / 2 * SCALE, self.size / 2 * SCALE]
		)

		for data in self.newBoxData:
			quat = [ 0.7071068, 0, 0, 0.7071068 ]
			vec = [data[0] - self.center[0], data[1] - self.center[1], data[2] - self.center[2]]
			newVec = vmath.rotate(vmath.vec3(vec), vmath.quat(quat))
			newPos = [newVec.x + self.center[0], newVec.y + self.center[1], newVec.z + self.center[2]]
			body = p.createMultiBody(
				baseMass=0, baseCollisionShapeIndex=shape, basePosition=newPos
			)
			p.changeDynamics(
				bodyUniqueId=body,
				linkIndex=-1,
				mass=0,
				linearDamping=0.4,
				angularDamping=1,
				restitution=0.8,
			)
			self.bodies.append(body)
	
	def SaveResult(self):
		"""
		This will save all activated body into a file.\n
		In next game loop, this final scene will read data from it and won't update\n
		any body in it.
		"""
		activated = list()
		activated.extend(self.removedBodies)
		for activatedBody in self.activatedBodies:
			if activatedBody in self.bodies:
				index = self.bodies.index(activatedBody)
				if index not in activated:
					activated.append(index)

		with open("TestVoxel/activatedBodies.pickle", "wb") as f:
			pickle.dump(activated, f)
	
	
	def HandleRemovedBodies(self):
		if not os.path.exists("TestVoxel/activatedBodies.pickle"):
			return

		with open("TestVoxel/activatedBodies.pickle", "rb") as f:
			removedIndex = pickle.load(f)
		self.removedBodies = removedIndex
		
		for removedBody in removedIndex:
			body = self.bodies[removedBody]
			p.removeBody(body)
			self.bodies[removedBody] = None
			self.model.setJoint(removedBody + 1, position=vmath.vec3(0,0,0))
			self.activatedBodies.append(body)
	
	def Destroy(self):
		self.showcase.remove(self.model)
		self.model = None