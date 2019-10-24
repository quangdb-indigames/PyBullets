import pyxie
from pyxie import devtool
import pickle
import pyvmath as vmath
import pybullet as p
import os

INIT_STATE = "INIT_STATE"
ACTIVE_STATE = "ACTIVE_STATE"
class FinalScene:
	def __init__(self, showcase):
		# Variable
		self.state = INIT_STATE
		self.showcase = showcase
		self.sizeMulti = 50

		#Init process
		self.VoxelModelProcess()
		self.ConstructPybulletProcess()

		#Activate process
		self.state = ACTIVE_STATE
		self.PyxieDisplayProcess()
		

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
			pos, rot = p.getBasePositionAndOrientation(bd)
			self.model.setJoint(index, position=vmath.vec3(pos), rotation=vmath.quat(rot), scale=vmath.vec3(self.sizeMulti, self.sizeMulti, self.sizeMulti ))
			index += 1

	def VoxelModelProcess(self):
		# ------------------------------------------------------------
		# --pre process

		FILENAME = "TestVoxel/Lion_Voxel_340_03.dae"

		if os.path.exists("TestVoxel/boxinfo.pickle"):
			os.remove("TestVoxel/boxinfo.pickle")

		if not os.path.exists("TestVoxel/boxinfo.pickle"):
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
			self.newBoxData = self.HandleBoxData(boxinfo)

			with open("TestVoxel/boxinfo.pickle", "wb") as f:
				pickle.dump(boxinfo, f)

			efig.mergeMesh()
			efig.saveFigure("TestVoxel/Lion_Enemy")
		# ------------------------------------------------------------

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
		translate = [0, 30, 3.6]
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
				mass=1,
				linearDamping=0.4,
				angularDamping=1,
				restitution=0.8,
			)
			self.bodies.append(body)