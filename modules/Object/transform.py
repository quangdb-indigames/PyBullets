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

		self.localPosition = position
		self.localRotation = rotation
		self.localScale = scale

		self.showOnInspector("localPosition")
		self.showOnInspector("localRotation")
		self.showOnInspector("localScale")
		self.kEpsilon = 0.000001
	
	def update(self):
		super().update()
		self.__autoTransformBaseParent()
	
	def setParent(self, newParent):
		try:
			newParent.childs.append(self.gameObject)
			self.gameObject.parent = newParent

			localPosition, localRotation, localScale = newParent.transform.fromWorldToLocalTransform(self)
			self.localPosition = localPosition
			self.localRotation = localRotation
			self.localScale = localScale
		except AttributeError:
			print("New parent is not of type GameObject!!!")

	def removeParent(self):
		self.gameObject.parent.childs.remove(self.gameObject)
		self.gameObject.parent = None

		# Local transform
		self.localPosition = self.position
		self.localScale = self.scale
		self.localRotation = self.rotation

	def __autoTransformBaseParent(self):
		if self.gameObject.parent is None:
			return

		position, rotation, scale = self.gameObject.parent.transform.fromLocalToWorldTransform(self)
		self.position = position
		self.rotation = rotation
		self.scale = scale
	
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
		childWorldMatrix = self.constructMatrixTransform(childTransform.position, childTransform.rotation, childTransform.scale)

		parentWorldInverseMatrix = self.constructMatrixTransform(self.position, self.rotation, self.scale)
		parentWorldInverseMatrix = vmath.inverse(parentWorldInverseMatrix)

		childLocalMatrix = vmath.mul(parentWorldInverseMatrix, childWorldMatrix)

		# Then decomposing the matrix transform into local position, local rotation, local scale
		localPosition, localRotation, localScale =  self.decomposeMatrixTransform(childLocalMatrix)

		return localPosition, localRotation, localScale

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
		cMT, cMR, cMS = self.constructMatrixTransform(childTransform.localPosition, childTransform.localRotation, childTransform.localScale, 2)
		MT, MR, MS = self.constructMatrixTransform(self.position, self.rotation, self.scale, 2)

		# Testing
		parentMatrix = self.constructMatrixTransform(self.position, self.rotation, self.scale)
		childTrans = vmath.mul(parentMatrix, cMT)

		pTrans = vmath.mul(MT, MR)
		cTrans = vmath.mul(cMT, cMR)
		temp = vmath.mul(MS, cMS)
		childGlobalMatrix = vmath.mul(pTrans, cTrans)
		childGlobalMatrix = vmath.mul(childGlobalMatrix, temp)

		# Then decomposing the matrix transform into global position, global rotation, global scale
		position, rotation, scale =  self.decomposeMatrixTransform(childGlobalMatrix)
		position = self.decomposeMatrixTranslate(childTrans)

		return position, rotation, scale


	def constructMatrixTransform(self, position, rotation, scale, result=1):
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

		# Last is rotation
		# Rotation matrix will become a 3x3 matrix
		# |m00 / scale.x    m10 / scale.y    m20 / scale.z|
		# |m01 / scale.x    m11 / scale.y    m21 / scale.z|
		# |m02 / scale.x    m12 / scale.y    m22 / scale.z|

		# From that, rotation.x = atan2 (m12/scale.y, m22/scale.z)
		radianX = math.atan2(matrixTransform.m12 / scaleY, matrixTransform.m22 / scaleZ)

		# rotation.y = atan2 (-m02 / scale.x, length(m12/scale.y, m22/scale.z))
		tempLength = vmath.length(vmath.vec2(matrixTransform.m12 / scaleY, matrixTransform.m22 / scaleZ))
		radianY = math.atan2(-matrixTransform.m02 / scaleX, tempLength)

		# rotation.z =  atan2 (m01 / scale.x, m00 / scale.x)
		radianZ = math.atan2(matrixTransform.m01 / scaleX, matrixTransform.m00 / scaleX)

		# Finally, convert to degrees
		rotation = [math.degrees(radianX), math.degrees(radianY), math.degrees(radianZ)]

		return position, rotation, scale

	def decomposeMatrixTranslate(self, matrixTransform):
		position = [matrixTransform.m30, matrixTransform.m31, matrixTransform.m32]
		return position

