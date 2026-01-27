bl_info = {
    "name": "Cities Skylines 2 UV Helper",
    "author": "Brian Chodur",
    "version": (1, 0, 0),
    "blender": (4, 3, 0),
    "location": "3D View > Sidebar > Cities Skylines 2 UV Helper",
    "description": "A toolset for creating and managing UV for Cities Skylines 2 assets.",
    "category": "3D View",
}

from . import panels, properties, operators

modules = [panels, properties, operators]

def register():
    for m in modules:
        m.register()

def unregister():
    for m in reversed(modules):
        m.unregister()

if __name__ == "__main__":
    register()
