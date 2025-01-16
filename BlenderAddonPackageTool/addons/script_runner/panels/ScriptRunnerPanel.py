import bpy

from addons.script_runner.config import __addon_name__
import bpy


class PT_ScriptRunner(bpy.types.Panel):
    bl_label = "Script Runner Panel"
    bl_idname = "VIEW3D_PT_SCRIPTRUNNER"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    # name of the side panel
    bl_category = "Script Runner"

    def draw(self, context: bpy.types.Context):
        addon_prefs = context.preferences.addons[__addon_name__].preferences
        layout = self.layout
        scene = bpy.context.scene

        row = layout.row()
        asset_slot = row.prop(scene.script_runner, "asset_path")

        row = layout.row()
        op = row.operator("scene_maker.falling_animation", text="Falling Animation")

        row = layout.row()
        op = row.operator("scene_maker.falling_animation_two", text="Falling Animation 2")

