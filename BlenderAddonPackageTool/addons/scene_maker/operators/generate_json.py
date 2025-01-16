import bpy

from addons.scene_maker.config import __addon_name__
from addons.scene_maker.functions.convert_scene_to_json import convert_scene_to_json
from addons.scene_maker.functions.get_camera_parameters import get_camera_parameters
from addons.scene_maker.functions.print_python_console import print_python_console

# This Example Operator will scale up the selected object
class OT_GenerateJson(bpy.types.Operator):
    bl_idname = "scene_maker.generate_json"
    bl_label = "Generate Json"

    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = bpy.context.scene
        render_camera = scene.scene_maker.render_camera
        if render_camera == "":
            print_python_console("No camera")
            return {'INVOKE'}
        convert_scene_to_json(render_camera)
        get_camera_parameters(render_camera)
        return {'FINISHED'}
