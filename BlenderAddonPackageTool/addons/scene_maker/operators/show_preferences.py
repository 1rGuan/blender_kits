import bpy
from addons.scene_maker.config import __addon_name__

class OT_ShowPreferences(bpy.types.Operator):
    bl_idname = "scene_maker.show_preferences"
    bl_label = "Show Preferences"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        bpy.ops.screen.userpref_show("INVOKE_DEFAULT")
        context.preferences.active_section  = "ADDONS"
        bpy.ops.preferences.addon_expand(module = __addon_name__)
        bpy.ops.preferences.addon_show(module = __addon_name__)
        return {'FINISHED'}
