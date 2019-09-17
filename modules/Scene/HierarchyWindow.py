import imgui
from modules.Scene.InspectorWindow import InspectorWindow
from modules.Object.game_object import GameObject
class HierarchyWindow():
	def __init__(self, position=[4,8], width=100, height=150):
		self.position = position
		self.width = width
		self.height = height
		self.inspector = InspectorWindow()
		self.curControlObject = None

	def update(self, curSceneGOs):
		imgui.set_next_window_position(self.position[0], self.position[1])
		imgui.set_next_window_size(self.width, self.height)
		imgui.begin("Hierarchy")

		for obj in curSceneGOs:
			self.displayGameObjectOnHierarchy(obj)
		imgui.end()

		if self.curControlObject != None and isinstance(self.curControlObject, GameObject):
			self.inspector.displayInspector(self.curControlObject)

	def displayGameObjectOnHierarchy(self, obj):
		if len(obj.childs) <= 0:
			if imgui.selectable(obj.name)[1]:
				self.curControlObject = obj
		else:
			object_layer = imgui.tree_node(obj.name, flags= imgui.TREE_NODE_OPEN_ON_ARROW)
			clicked = imgui.is_item_clicked()
			if clicked:
				self.curControlObject = obj
			
			if object_layer:			
				for childObj in obj.childs:
					self.displayGameObjectOnHierarchy(childObj)
				imgui.tree_pop()