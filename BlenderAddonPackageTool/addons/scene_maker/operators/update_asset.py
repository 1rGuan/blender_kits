import bpy
from addons.scene_maker.functions.add_asset_libraries import add_asset_libraries

class OT_UpdateAsset(bpy.types.Operator):
    bl_idname = "scene_maker.update_asset"
    bl_label = "Update asset"
    bl_options = {'REGISTER'}

    def execute(self, context):
        self.report({'INFO'}, "Confirmed!")
        add_asset_libraries()
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="本操作将会清空场景和资产库中的所有内容", icon='ERROR')
