import math
import pyvmath as vmath
def fromEulerToQuaternion(euler):
	# XZY
	x, y, z = math.radians(euler[0] % 360), math.radians(euler[1] % 360), math.radians(euler[2] % 360)

	cy = math.cos(z * 0.5)
	sy = math.sin(z * 0.5)
	cp = math.cos(y * 0.5)
	sp = math.sin(y * 0.5)
	cr = math.cos(x * 0.5)
	sr = math.sin(x * 0.5)

	q = list()
	qw = cy * cp * cr + sy * sp * sr
	qx = cy * cp * sr - sy * sp * cr
	qy = sy * cp * sr + cy * sp * cr
	qz = sy * cp * cr - cy * sp * sr

	q.append(qx)
	q.append(qy)
	q.append(qz)
	q.append(qw)
	return q

def displayGameObjectTransformSetting(obj, imgui):
	if obj.parent is not None:
		# If this object is child of other game object, display it local transform
		changed, obj.transform.localPosition = imgui.drag_float3(
			"position", *obj.transform.localPosition, format="%.1f", change_speed = 0.05
		)
		if changed:
			obj.update()

		# Setting rotation
		changed, obj.transform.localRotation = imgui.drag_float3(
			"rotation", *obj.transform.localRotation, format="%.2f", change_speed = 0.5
		)				
		if changed:
			obj.update()

		# Setting scale
		changed, obj.transform.localScale = imgui.drag_float3(
			"scale", *obj.transform.localScale, format="%.1f", change_speed = 0.05
		)
		if changed:
			obj.update()
	else:
		# Else display it global transform
		changed, obj.transform.position = imgui.drag_float3(
			"position", *obj.transform.position, format="%.1f", change_speed = 0.05
		)
		if changed:
			obj.update()

			# Setting rotation
		changed, obj.transform.rotation = imgui.drag_float3(
			"rotation", *obj.transform.rotation, format="%.2f", change_speed = 0.5
		)				
		if changed:
			obj.update()

			# Setting scale
		changed, obj.transform.scale = imgui.drag_float3(
			"scale", *obj.transform.scale, format="%.1f", change_speed = 0.05
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
		return
		
	if isinstance(component.__dict__[attrName], bool):
		displayBoolAttribute(imgui, component, attrName)
		return
	
	if isinstance(component.__dict__[attrName], float):
		displayListFloatAttribute(imgui, component, attrName)
		return
	elif isinstance(component.__dict__[attrName], (list, tuple)) and isinstance(component.__dict__[attrName][0], (float)):
		displayListFloatAttribute(imgui, component, attrName)
		return
	
	if isinstance(component.__dict__[attrName], int):
		displayListIntAttribute(imgui, component, attrName)
		return
	elif isinstance(component.__dict__[attrName], (list, tuple)) and isinstance(component.__dict__[attrName][0], (int)):
		displayListIntAttribute(imgui, component, attrName)
		return

	

def displayBoolAttribute(imgui, component, attrName):
	changed, component.__dict__[attrName] = imgui.checkbox(
		attrName.capitalize(),
		component.__dict__[attrName]
	)

	if changed:
		component.update()

def displayTextAttribute(imgui, component, attrName):
	changed, component.__dict__[attrName] = imgui.input_text(
		attrName.capitalize(),
		component.__dict__[attrName],
		256
	)

	if changed:
		component.update()

def displayListFloatAttribute(imgui, component, attrName):
	changed = False
	if isinstance(component.__dict__[attrName], float):
		changed, component.__dict__[attrName] = imgui.drag_float(
			attrName, component.__dict__[attrName], format="%.2f", change_speed = 0.05
		)
		if changed:
			component.update()
		return
		
	if len(component.__dict__[attrName]) == 0:
		return

	if len(component.__dict__[attrName]) == 2:
		changed, component.__dict__[attrName] = imgui.drag_float2(
			attrName, *component.__dict__[attrName], format="%.2f", change_speed = 0.05
		)
	elif len(component.__dict__[attrName]) == 3:
		changed, component.__dict__[attrName] = imgui.drag_float3(
			attrName, *component.__dict__[attrName], format="%.2f", change_speed = 0.05
		)
	elif len(component.__dict__[attrName]) == 4:
		changed, component.__dict__[attrName] = imgui.drag_float4(
			attrName, *component.__dict__[attrName], format="%.2f", change_speed = 0.05
		)
	else:
		imgui.text(attrName)
		for i in range(0, len(component.__dict__[attrName])):
			changed, component.__dict__[attrName][i] = imgui.drag_float(
				str(i+1), component.__dict__[attrName][i], format="%.2f", change_speed = 0.05
			)

			if changed:
				component.update()
	
	if changed:
		component.update()

def displayListIntAttribute(imgui, component, attrName):
	changed = False
	if isinstance(component.__dict__[attrName], int):
		changed, component.__dict__[attrName] = imgui.drag_int(
			attrName, component.__dict__[attrName]
		)
		if changed:
			component.update()
		return
		
	if len(component.__dict__[attrName]) == 0:
		return

	if len(component.__dict__[attrName]) == 2:
		changed, component.__dict__[attrName] = imgui.drag_int2(
			attrName, *component.__dict__[attrName]
		)
	elif len(component.__dict__[attrName]) == 3:
		changed, component.__dict__[attrName] = imgui.drag_int3(
			attrName, *component.__dict__[attrName]
		)
	elif len(component.__dict__[attrName]) == 4:
		changed, component.__dict__[attrName] = imgui.drag_int4(
			attrName, *component.__dict__[attrName]
		)
	else:
		imgui.text(attrName)
		for i in range(0, len(component.__dict__[attrName])):
			changed, component.__dict__[attrName][i] = imgui.drag_int(
				str(i+1), component.__dict__[attrName][i]
			)

			if changed:
				component.update()
	
	if changed:
		component.update()

def getObjectOfType(objType, listObjs):
	for obj in listObjs:
		if isinstance(obj, objType):
			return obj
	return None
