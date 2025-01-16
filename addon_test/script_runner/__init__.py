from .addons.script_runner import register as addon_register, unregister as addon_unregister

bl_info = {
    "name": 'Script Runner',
    "author": 'ez',
    "blender": (4, 2, 0),
    "version": (0, 0, 1),
    "description": 'The plugin to run scripts quickly',
    "warning": '',
    "support": 'COMMUNITY',
    "category": '3D View'
}

def register():
    addon_register()

def unregister():
    addon_unregister()

    