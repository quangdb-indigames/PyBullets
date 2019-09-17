import imgui
from modules.Helper import helperFunction as HELPER
class InspectorWindow():
	def __init__(self, position=[5, 160], width=150, height=100):
		self.position = position
		self.width = width
		self.height = height

	def displayInspector(self, obj):
		imgui.set_next_window_position(self.position[0], self.position[1])
		imgui.set_next_window_size(self.width, self.height)

		expanded, opened = imgui.begin("Inspector", True)
		if opened:
			imgui.begin_group()
			imgui.bullet_text(obj.name)

			transform_layer, visible = imgui.collapsing_header("Transform", True)
			if transform_layer:
				HELPER.displayGameObjectTransformSetting(obj, imgui)
			imgui.end_group()

			for component in obj.components:
				HELPER.displayComponentSetting(imgui, component, obj)
		imgui.end()