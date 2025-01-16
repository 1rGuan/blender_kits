import bpy
from addons.scene_maker.config import __addon_name__
from addons.scene_maker.functions.render_scene import render_scene
from addons.scene_maker.functions.convert_scene_to_json import convert_scene_to_json
from addons.scene_maker.functions.print_python_console import print_python_console

class OT_RenderScene(bpy.types.Operator):
    bl_idname = "scene_maker.render_scene"
    bl_label = "Render Scene"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        scene = bpy.context.scene
        author_name = scene.scene_maker.author_name
        scene_name = scene.scene_maker.scene_name
        scene_name_suffix = scene.scene_maker.scene_name_suffix
        output_path = scene.scene_maker.img_output_folder
        render_camera = scene.scene_maker.render_camera
        if render_camera == "":
            print_python_console("No camera")
            return {'INVOKE'}
        new_scene_name = f"{author_name}_{scene_name}_{scene_name_suffix}"
        render_scene(new_scene_name, output_path, render_camera)
        convert_scene_to_json(new_scene_name, render_camera)
        scene.scene_maker.scene_name_suffix += 1
        return {'FINISHED'}
