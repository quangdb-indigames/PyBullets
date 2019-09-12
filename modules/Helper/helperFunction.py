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

def displayGameObjectTransformSetting(obj, imgui):
	if obj.parent is not None:
		# If this object is child of other game object, display it local transform
		changed, obj.localPosition = imgui.drag_float3(
			"position", *obj.localPosition, format="%.1f", change_speed = 0.05
		)
		if changed:
			obj.update()

		# Setting rotation
		changed, obj.localRotation = imgui.drag_float3(
			"rotation", *obj.localRotation, format="%.2f", change_speed = 0.5
		)				
		if changed:
			obj.update()

		# Setting scale
		changed, obj.localScale = imgui.drag_float3(
			"scale", *obj.localScale, format="%.1f", change_speed = 0.05
		)
		if changed:
			obj.update()
	else:
		# Else display it global transform
		changed, obj.__dict__['position'] = imgui.drag_float3(
			"position", *obj.__dict__['position'], format="%.1f", change_speed = 0.05
		)
		if changed:
			obj.update()

			# Setting rotation
		changed, obj.rotation = imgui.drag_float3(
			"rotation", *obj.rotation, format="%.2f", change_speed = 0.5
		)				
		if changed:
			obj.update()

			# Setting scale
		changed, obj.scale = imgui.drag_float3(
			"scale", *obj.scale, format="%.1f", change_speed = 0.05
		)
		if changed:
			obj.update()

def displayComponentSetting(imgui, component):
	imgui.begin_group()
	try:
		component_layer, visible = imgui.collapsing_header(component.__class__.__name__, True)
	except:
		print("Layer creating failed!")
	if component_layer:
		for displayAttr in component.listAttrToShow:
			try:
				displayAttributeOnInspector(imgui, component, displayAttr)
			except:
				print("displayAttributeOnInspector failed!")
					
	imgui.end_group()

def displayAttributeOnInspector(imgui, component, attrName):
	if isinstance(component.__dict__[attrName], str):
		displayTextAttribute(imgui, component, attrName)

def displayTextAttribute(imgui, component, attrName):
	changed, component.__dict__[attrName] = imgui.input_text(
		attrName.capitalize(),
		component.__dict__[attrName],
		256
	)

def getObjectOfType(objType, listObjs):
	for obj in listObjs:
		if isinstance(obj, objType):
			return obj
	return None