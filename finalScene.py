import pyxie
from pyxie import devtool
import pickle
import pyvmath as vmath
import pybullet as p
import os

INIT_STATE = "INIT_STATE"
ACTIVE_STATE = "ACTIVE_STATE"
class FinalScene:
	def __init__(self):
		self.state = INIT_STATE
		self.VoxelModelProcess()
		self.ConstructPybulletProcess()

	def Update(self):
		if self.state == INIT_STATE:
			return
		
		

	def VoxelModelProcess(self):
		# ------------------------------------------------------------
		# --pre process

		FILENAME = "TestVoxel/Lion_Voxel_340_02.dae"

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
		# Min y
		minY = boxData[0][0][1]
		# Min z
		minZ = boxData[0][0][2]

		for point in boxData:
			if point[0][0] < minX:
				minX = point[0][0]
			if point[0][1] < minY:
				minY = point[0][1]
			if point[0][2] < minZ:
				minZ = point[0][2]
		
		root = [minX, minY, minZ]

		matrixList = self.Matrilization(root, self.size, boxData)
		self.size *= 5
		newBoxData = self.CalculatePositionWithNewSize(root, matrixList, self.size)
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
			pos = (data[0], data[1], data[2] + 0.1)
			body = p.createMultiBody(
				baseMass=0, baseCollisionShapeIndex=shape, basePosition=pos
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