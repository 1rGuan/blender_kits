import bpy
from addons.scene_maker.functions.clear_all_asset_libraries import clear_all_asset_libraries
from addons.scene_maker.functions.add_asset_libraries import add_asset_libraries

class OT_InitializePlugin(bpy.types.Operator):
    bl_idname = "scene_maker.initialize_plugin"
    bl_label = "Initialize Scene Maker Plugin"
    bl_options = {'REGISTER'}

    def execute(self, context):
        clear_all_asset_libraries()
        add_asset_libraries()
        bpy.ops.script.reload()
        print("Scene Maker initialized")
        return {'FINISHED'}
