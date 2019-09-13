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
    
    def update(self):
        super().update()
    
    def fromWorldToLocalTransform(childWorldTransform):
        """
		Calculate local transform relate to this transform
			Parameters
			----------
			childWorldTransform: Transform
				transform of the object need to calculate
			Returns
			-------
            local transform relate to this object
		"""
        # From global transform -> local transform
        # Local<T> = Global<T, Child> * inverse.Global<T, Parent>
        childWorldMatrix = self.constructMatrixTransform(childWorldTransform.position, childWorldTransform.rotation, childWorldTransform.scale)
        parentWorldInverseMatrix = self.constructMatrixTransform(self.position, self.rotation, self.scale)
        parentWorldInverseMatrix = vmath.inverse(parentWorldInverseMatrix)

        childLocalMatrix = vmath.mul(childWorldMatrix, parentWorldInverseMatrix)

        # Then decomposing the matrix transform into local position, local rotation, local scale
        localPosition, localRotation, localScale =  self.decomposeMatrixTransform(childLocalMatrix)

        return localPosition, localRotation, localScale

    def constructMatrixTransform(position, rotation, scale):
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
        matrixScale = vmath.mat_scale(vmath.vec3(scale), 4)
        matrixTranslation = vmath.mat_translation(vmath.vec3(position))

        radX = math.radians(rotation[0] % 360)
        radY = math.radians(rotation[1] % 360)
        radZ = math.radians(rotation[2] % 360)
        matrixRotation = vmath.mat_rotationZYX(radX, radY, radZ)

        matrixTransform = vmath.mul(matrixScale, matrixTranslation)
        matrixTransform = vmath.mul(matrixTransform, matrixRotation)
        return matrixTransform

    def decomposeMatrixTransform(matrixTransform):
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
        # |m00  m01  m02  m03|
        # |m10  m11  m12  m13|
        # |m20  m21  m22  m23|
        # | 0    0    0    1 |

        # position will be [m03, m13, m23]
        position = [matrixTransform.m03, matrixTransform.m13, matrixTransform.m23]

        # scale will be
        # scale.x = length(m00, m10, m20)
        # scale.y = length(m01, m11, m21)
        # scale.z = length(m02, m12, m22)
        scaleX = vmath.length(vmath.vec3(matrixTransform.m00, matrixTransform.m10, matrixTransform.m20))
        scaleY = vmath.length(vmath.vec3(matrixTransform.m01, matrixTransform.m11, matrixTransform.m21))
        scaleZ = vmath.length(vmath.vec3(matrixTransform.m02, matrixTransform.m12, matrixTransform.m22))

        scale = [scaleX, scaleY, scaleZ]

        # Last is rotation
        # Rotation matrix will become a 3x3 matrix
        # |m00 / scale.x    m01 / scale.y    m02 / scale.z|
        # |m10 / scale.x    m11 / scale.y    m12 / scale.z|
        # |m20 / scale.x    m21 / scale.y    m22 / scale.z|

        # From that, rotation.x = atan2 (m21/scale.y, m22/scale.z)
        radianX = math.atan2(matrixTransform.m21 / scaleY, matrixTransform.m22 / scaleZ)

        # rotation.y = atan2 (-m20 / scale.x, length(m21/scale.y, m22/scale.z))
        tempLength = vmath.length(vmath.vec2(matrixTransform.m21 / scaleY, matrixTransform.m22 / scaleZ))
        radianY = math.atan2(-matrixTransform.m20 / scaleX, tempLength)

        # rotation.z =  atan2 (m10 / scale.x, m00 / scale.x)
        radianZ = math.atan2(matrixTransform.m10 / scaleX, matrixTransform.m00 / scaleX)

        # Finally, convert to degrees
        rotation = [math.degrees(radianX), math.degrees(radianY), math.degrees(radianZ)]

        return position, rotation, scale


