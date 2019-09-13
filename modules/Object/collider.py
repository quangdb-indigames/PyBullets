from modules.Object.component import Component
class Collider(Component):
    def __init__(self, gameObject):
        super().__init__(gameObject)
    
    def update(self):
        super().update()
    
    def onCollisionContact(self, other):
        pass