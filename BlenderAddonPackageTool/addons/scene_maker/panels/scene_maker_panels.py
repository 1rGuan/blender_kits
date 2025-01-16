import bpy

from addons.scene_maker.config import __addon_name__
from common.i18n.i18n import i18n
import bpy


class PT_SceneMakerPanel(bpy.types.Panel):
    bl_label = "Scene Maker"
    bl_idname = "VIEW3D_PT_SCENEMAKER"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    # name of the side panel
    bl_category = "Scene Maker"

    def draw(self, context: bpy.types.Context):
        addon_prefs = context.preferences.addons[__addon_name__].preferences
        layout = self.layout
        scene = bpy.context.scene

        row = layout.row()
        op = row.operator("scene_maker.show_preferences", text="打开基础设置")

        layout.label(text="")
        basic_info_label = layout.row()
        basic_info_label.label(text="基本信息", icon="SETTINGS")
        author_name_slot = layout.row()
        author_name_slot.prop(scene.scene_maker, "author_name")
        scene_name_slot = layout.row()
        scene_name_slot.prop(scene.scene_maker, "scene_name")

        layout.label(text="")
        basic_info_label = layout.row()
        basic_info_label.label(text="渲染设置", icon="SHADING_RENDERED")
        render_camera_slot = layout.row()
        render_camera_slot.prop(scene.scene_maker, "render_camera")
        img_output_folder_slot = layout.row()
        img_output_folder_slot.prop(scene.scene_maker, "img_output_folder")
        row = layout.row()
        op = row.operator("scene_maker.render_scene", text="渲染场景")

        # layout.label(text="")
        # json_generate_label = layout.row()
        # json_generate_label.label(text="JSON生成相关", icon="TEXT")
        # json_path_slot = layout.row()
        # json_path_slot.prop(scene.scene_maker, "json_path")
        # row = layout.row()
        # op = row.operator("scene_maker.generate_json", text="生成JSON")

        layout.label(text="")
        asset_manage_label = layout.row()
        asset_manage_label.label(text="资产管理相关", icon="ASSET_MANAGER")
        row = layout.row()
        row.prop(scene.scene_maker, "asset_path")
        row = layout.row()
        op = row.operator("scene_maker.update_asset", text="更新资产")
        
        layout.label(text="")
        script_path_slot = layout.row()
        script_path_slot.prop(scene.scene_maker, "script_path")
        row = layout.row()
        op = row.operator("scene_maker.run_script", text="执行脚本")
        

    # @classmethod
    # def poll(cls, context: bpy.types.Context):
    #     return context.active_object is not None

