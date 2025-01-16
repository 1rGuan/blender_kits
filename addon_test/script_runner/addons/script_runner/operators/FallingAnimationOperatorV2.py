import bpy

from script_runner.addons.script_runner.functions.falling_animation_version_two import falling_animation_version_two

class OT_FallingAnimationVersionTwo(bpy.types.Operator):
    bl_idname = "scene_maker.falling_animation_two"
    bl_label = "Test Two"

    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = bpy.context.scene
        falling_animation_version_two()
        return {'FINISHED'}
