import os
import bpy
from addons.scene_maker.config import __addon_name__

class SceneMakerPreference(bpy.types.AddonPreferences):
    bl_idname = __addon_name__

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        scene = bpy.context.scene
        layout.label(text="Scene Maker Plugin")
        
        layout.prop(scene.scene_maker, "author_name")
        layout.prop(scene.scene_maker, "asset_path")
        # layout.prop(scene.scene_maker, "json_path")
        layout.prop(scene.scene_maker, "img_output_folder")
        row = layout.row()
        op = row.operator("scene_maker.initialize_plugin", text="应用设置")
