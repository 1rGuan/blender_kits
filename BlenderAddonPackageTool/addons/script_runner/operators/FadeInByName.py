import bpy

from addons.script_runner.functions.fade_in_by_name import fade_in_by_name

# This Example Operator will scale up the selected object
class OT_FadeInByName(bpy.types.Operator):
    bl_idname = "scene_maker.fade_in_by_name"
    bl_label = "Test One"

    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = bpy.context.scene
        fade_in_by_name()
        return {'FINISHED'}