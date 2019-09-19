import pyvmath as vmath
import math
from modules.Object.component import Component
from modules.Helper import helperFunction
class Transform(Component):
	def __init__(self, gameObject, position=[0.0,0.0,0.0], rotation=[0.0,0.0,0.0], scale=[1.0, 1.0, 1.0]):
		super().__init__(gameObject)

		self.position = position
		self.rotation = rotation
		self.scale = scale
		self.shear = vmath.mat44([
			1, 0, 0, 0,
			0, 1, 0, 0,
			0, 0, 1, 0,
			0, 0, 0, 1
		])

		self.localPosition = position
		self.localRotation = rotation
		self.localScale = scale
		self.localShear = vmath.mat44([
			1, 0, 0, 0,
			0, 1, 0, 0,
			0, 0, 1, 0,
			0, 0, 0, 1
		])

		self.showOnInspector("localPosition")
		self.showOnInspector("localRotation")
		self.showOnInspector("localScale")
		self.kEpsilon = 0.000001
	
	def update(self):
		super().update()
		self.__autoTransformBaseParent()
	
	def setParent(self, newParent):
		# try:
			newParent.childs.append(self.gameObject)
			self.gameObject.parent = newParent

			localPosition, localRotation, localScale, localShear = newParent.transform.fromWorldToLocalTransform(self)
			self.localPosition = localPosition
			self.localRotation = localRotation
			self.localScale = localScale
			self.localShear = localShear
		# except AttributeError:
		# 	print("New parent is not of type GameObject!!!")

	def removeParent(self):
		self.gameObject.parent.childs.remove(self.gameObject)
		self.gameObject.parent = None

		# Local transform
		self.localPosition = self.position
		self.localScale = self.scale
		self.localRotation = self.rotation
		self.localShear = self.shear

	def __autoTransformBaseParent(self):
		if self.gameObject.parent is None:
			return

		position, rotation, scale, shear = self.gameObject.parent.transform.fromLocalToWorldTransform(self)
		self.position = position
		self.rotation = rotation
		self.scale = scale
		self.shear - shear
	
	def fromWorldToLocalTransform(self, childTransform):
		"""
		Calculate local transform relate to this transform
			Parameters
			----------
			childTransform: Transform
				transform of the object need to calculate
			Returns
			-------
			local transform relate to this object
		"""
		# From global transform -> local transform
		# Local<T> = inverse.Global<T, Parent> * Global<T, Child>
		childWorldMatrix = self.constructMatrixTransform(childTransform.position, childTransform.rotation, childTransform.scale, childTransform.shear)

		parentWorldInverseMatrix = self.constructMatrixTransform(self.position, self.rotation, self.scale, self.shear)
		parentWorldInverseMatrix = vmath.inverse(parentWorldInverseMatrix)

		childLocalMatrix = vmath.mul(parentWorldInverseMatrix, childWorldMatrix)

		# Then decomposing the matrix transform into local position, local rotation, local scale
		localPosition, localRotation, localScale, localShear =  self.decomposeMatrixTransformationType(childLocalMatrix)

		return localPosition, localRotation, localScale, localShear

	def fromLocalToWorldTransform(self, childTransform):
		"""
		Calculate child global transform base on this game object transform and child local transform
			Parameters
			----------
			childTransform: Transform
				local transform of the child relative to this game object
			Returns
			-------
			global transform of child
		"""
		# From local -> global
		# Global<T> = Global<T, parent> * Local<T, child>
		# cMT, cMR, cMS = self.constructMatrixTransform(childTransform.localPosition, childTransform.localRotation, childTransform.localScale, 2)
		# MT, MR, MS = self.constructMatrixTransform(self.position, self.rotation, self.scale, 2)

		childLocalMatrix = self.constructMatrixTransform(childTransform.localPosition, childTransform.localRotation, childTransform.localScale, childTransform.localShear)
		parentGlobalMatrix = self.constructMatrixTransform(self.position, self.rotation, self.scale, self.shear)

		childGlobalMatrix = vmath.mul(parentGlobalMatrix, childLocalMatrix)
		# # Testing
		# parentMatrix = self.constructMatrixTransform(self.position, self.rotation, self.scale)
		# childTrans = vmath.mul(parentMatrix, cMT)

		# childScale = vmath.mul(parentMatrix, vmath.vec3(childTransform.localScale))
		# print("Child scale is: ", childScale)

		# pTrans = vmath.mul(MT, MR)
		# cTrans = vmath.mul(cMT, cMR)
		# temp = vmath.mul(MS, cMS)
		# childGlobalMatrix = vmath.mul(pTrans, cTrans)
		# childGlobalMatrix = vmath.mul(childGlobalMatrix, temp)



		# Then decomposing the matrix transform into global position, global rotation, global scale
		position, rotation, scale, shear =  self.decomposeMatrixTransformationType(childGlobalMatrix)
		
		# testPos, testRot, testScale = self.decomposeMatrixTransformationType(childGlobalMatrix)

		return position, rotation, scale, shear


	def constructMatrixTransform(self, position, rotation, scale, matrixShear, result=1):
		"""
		Construct a 4x4 matrix transform from position, rotation, scale
			Parameters
			----------
			position: list of 3
				position of object
			rotation: list of 3
				rotation of object, in euler angle (degrees)
			scale: list of 3
				scale of object
			Returns
			-------
			A 4x4 matrix transform (in vmath.mat44)
		"""
		matrixScale = vmath.mat_scale(4, vmath.vec3(scale))

		matrixTranslation = vmath.mat_translation(vmath.vec3(position))
		
		radX = math.radians(rotation[0] % 360)
		radY = math.radians(rotation[1] % 360)
		radZ = math.radians(rotation[2] % 360)
		matrixRotation = vmath.mat_rotationZYX(4, [radX, radY, radZ])

		matrixTransform = vmath.mul(matrixTranslation, matrixRotation)
		matrixTransform = vmath.mul(matrixTransform, matrixShear)
		matrixTransform = vmath.mul(matrixTransform, matrixScale)
		if result==2:
			return matrixTranslation, matrixRotation, matrixScale
		else:
			return matrixTransform

	def decomposeMatrixTransform(self, matrixTransform):
		"""
		Decomposing a 4x4 matrix transform into position, rotation, scale
			----------
			Parameters
			----------
			matrixTransform: vmath.mat44
				transform matrix
			-------
			Returns
			-------
			position, rotation, scale
		"""

		# With a matrix transform 4x4
		# |m00  m10  m20  m30|
		# |m01  m11  m21  m31|
		# |m02  m12  m22  m32|
		# |m03  m13  m23  m33|

		# position will be [m03, m13, m23]
		position = [matrixTransform.m30, matrixTransform.m31, matrixTransform.m32]

		# scale will be
		# scale.x = length(m00, m01, m02)
		# scale.y = length(m10, m11, m12)
		# scale.z = length(m20, m21, m22)
		scaleX = vmath.length(vmath.vec3(matrixTransform.m00, matrixTransform.m01, matrixTransform.m02))
		scaleY = vmath.length(vmath.vec3(matrixTransform.m10, matrixTransform.m11, matrixTransform.m12))
		scaleZ = vmath.length(vmath.vec3(matrixTransform.m20, matrixTransform.m21, matrixTransform.m22))

		scale = [scaleX, scaleY, scaleZ]
		scale = self.roundVector3(scale)

		# Last is rotation
		# Rotation matrix will become a 3x3 matrix
		# |m00 / scale.x    m10 / scale.y    m20 / scale.z|
		# |m01 / scale.x    m11 / scale.y    m21 / scale.z|
		# |m02 / scale.x    m12 / scale.y    m22 / scale.z|


		matrixRotation = vmath.mat33(
			[
				matrixTransform.m00 / scale[0], matrixTransform.m01 / scale[0], matrixTransform.m02 / scale[0],
				matrixTransform.m10 / scale[1], matrixTransform.m11 / scale[1], matrixTransform.m12 / scale[1],
				matrixTransform.m20 / scale[2], matrixTransform.m21 / scale[2], matrixTransform.m22 / scale[2]
			]
		)

		# From that, rotation.x = atan2 (m12/scale.y, m22/scale.z)
		radianX = math.atan2(matrixTransform.m12 / scale[1], matrixTransform.m22 / scale[2])

		# rotation.y = atan2 (-m02 / scale.x, length(m12/scale.y, m22/scale.z))
		tempLength = vmath.length(vmath.vec2(matrixTransform.m12 / scale[1], matrixTransform.m22 / scale[2]))
		radianY = math.atan2(-matrixTransform.m02 / scale[0], tempLength)

		# rotation.z =  atan2 (m01 / scale.x, m00 / scale.x)
		radianZ = math.atan2(matrixTransform.m01 / scale[0], matrixTransform.m00 / scale[0])

		# Finally, convert to degrees
		rotation = [math.degrees(radianX), math.degrees(radianY), math.degrees(radianZ)]

		# # Testing
		# v0 = vmath.normalize(vmath.vec3(matrixTransform.getCol(0)))
		# v2 = vmath.normalize(vmath.cross(v0, vmath.vec3(matrixTransform.getCol(1))))
		# v1 = vmath.normalize(vmath.cross(v2, v0))
		# rotmat = vmath.mat33(v0,v1,v2)

		# radianX = math.atan2(rotmat.m12, rotmat.m22)
		# tempLength = vmath.length(vmath.vec2(rotmat.m12, rotmat.m22))
		# radianY = math.atan2(-rotmat.m02, tempLength)
		# radianZ = math.atan2(rotmat.m01, rotmat.m00)
		# rotation = [math.degrees(radianX), math.degrees(radianY), math.degrees(radianZ)]			

		return position, rotation, scale
	
	def decomposeMatrixTransformationType(self, matrixTransform):
		# With a matrix transform 4x4
		# |m00  m10  m20  m30|
		# |m01  m11  m21  m31|
		# |m02  m12  m22  m32|
		# |m03  m13  m23  m33|

		# position will be [m03, m13, m23]
		position = [matrixTransform.m30, matrixTransform.m31, matrixTransform.m32]

		col_0 = [matrixTransform.m00, matrixTransform.m01, matrixTransform.m02]
		col_1 = [matrixTransform.m10, matrixTransform.m11, matrixTransform.m12]
		col_2 = [matrixTransform.m20, matrixTransform.m21, matrixTransform.m22]

		# Compute X scale and normalize first col
		scaleX = vmath.length(vmath.vec3(col_0))
		col_0 = vmath.normalize(vmath.vec3(col_0))
		col_0 = [col_0.x, col_0.y, col_0.z]

		# Compute XY shear factor and make 2nd col orthogonal to 1st		
		shear_xy = vmath.dot(vmath.vec3(col_0), vmath.vec3(col_1))
		col_1 = self.linearCombine(col_1, col_0, 1.0, -shear_xy)
		
		# Compute Y scale
		scaleY = vmath.length(vmath.vec3(col_1))
		col_1 = vmath.normalize(vmath.vec3(col_1))
		col_1 = [col_1.x, col_1.y, col_1.z]

		shear_xy /= scaleY
		# Compute XZ and YZ shear
		shear_xz = vmath.dot(vmath.vec3(col_0), vmath.vec3(col_2))
		col_2 = self.linearCombine(col_2, col_0, 1.0, -shear_xz)
		shear_yz = vmath.dot(vmath.vec3(col_1), vmath.vec3(col_2))
		col_2 = self.linearCombine(col_2, col_1, 1.0, -shear_yz)

		# Next, get Z scale
		scaleZ = vmath.length(vmath.vec3(col_2))
		col_2 = vmath.normalize(vmath.vec3(col_2))
		col_2 = [col_2.x, col_2.y, col_2.z]

		# Check determinant
		# if vmath.dot(col_0, vmath.cross(col_1, col_2)) < 0:
		# 	scaleX *= -1
		# 	scaleY *= -1
		# 	scaleZ *= -1
		# 	col_0 = [-col_0[0], -col_0[1], -col_0[2]]
		# 	col_1 = [-col_1[0], -col_1[1], -col_1[2]]
		# 	col_2 = [-col_2[0], -col_2[1], -col_2[2]]
		
		scale = [scaleX, scaleY, scaleZ]

		rotationY = math.asin(-col_0[2])
		if (math.cos(rotationY) != 0):
			rotationX = math.atan2(col_1[2], col_2[2])
			rotationZ = math.atan2(col_0[1], col_0[0])
		else:
			rotationX = math.atan2(-col_2[0], col_1[1])
			rotationZ = 0
		
		rotation = [math.degrees(rotationX), math.degrees(rotationY), math.degrees(rotationZ)]

		shear = vmath.mat44([
			1, 0, 0, 0,
			shear_xy, 1, 0, 0,
			shear_xz, shear_yz, 1, 0,
			0, 0, 0, 1
		])

		return position, rotation, scale, shear



	def linearCombine(self, a, b, a1, b1):
		resultX = (a1 * a[0]) + (b1 * b[0])
		resultY = (a1 * a[1]) + (b1 * b[1])
		resultZ = (a1 * a[2]) + (b1 * b[2])

		return [resultX, resultY, resultZ]
		
		
	
	def roundVector3(self, vec):
		vec[0] = self.roundingFloat(vec[0])
		vec[1] = self.roundingFloat(vec[1])
		vec[2] = self.roundingFloat(vec[2])
		return vec
	
	def roundingFloat(self, roundNum):
		if abs(roundNum) <= self.kEpsilon:
			if roundNum <= 0:
				roundNum = -self.kEpsilon
			else:
				roundNum = self.kEpsilon
		return roundNum

	def decomposeMatrixTranslate(self, matrixTransform):
		position = [matrixTransform.m30, matrixTransform.m31, matrixTransform.m32]
		return position
	
	def decomposeMatrixScale(self, matrixTransform):
		scaleX = vmath.length(vmath.vec3(matrixTransform.m00, matrixTransform.m01, matrixTransform.m02))
		scaleY = vmath.length(vmath.vec3(matrixTransform.m10, matrixTransform.m11, matrixTransform.m12))
		scaleZ = vmath.length(vmath.vec3(matrixTransform.m20, matrixTransform.m21, matrixTransform.m22))

		scale = [scaleX, scaleY, scaleZ]
		scale = self.roundVector3(scale)

		return scale

