import math
def fromEulerToQuaternion(euler):
	# XZY
	x, y, z = math.radians(euler[0] % 360), math.radians(euler[1] % 360), math.radians(euler[2] % 360)

	cz = math.cos(z * 0.5)
	sz = math.sin(z * 0.5)
	cy = math.cos(y * 0.5)
	sy = math.sin(y * 0.5)
	cx = math.cos(x * 0.5)
	sx = math.sin(x * 0.5)

	q = list()
		
	qx = sx * cy * cz - cx * sy * sz		# x
	qy = cx * cy * sz + sx * sy * cz		# y
	qz = cx * sy * cz - sx * cy * sz		# z
	qw = cx * cy * cz + sx * sy * sz		# w
	q.append(qx)
	q.append(qy)
	q.append(qz)
	q.append(qw)
	return q