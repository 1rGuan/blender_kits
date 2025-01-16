import bpy

from addons.script_runner.functions.falling_animation import falling_animation

# This Example Operator will scale up the selected object
class OT_FallingAnimation(bpy.types.Operator):
    bl_idname = "scene_maker.falling_animation"
    bl_label = "Test One"

    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = bpy.context.scene
        falling_animation()
        return {'FINISHED'}
