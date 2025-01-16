import os
import bpy
from pathlib import Path

from addons.scene_maker.config import __addon_name__
from addons.scene_maker.i18n.dictionary import dictionary

from addons.scene_maker.properties import SceneMakerAddonProperties

from addons.scene_maker.operators.generate_json import OT_GenerateJson
from addons.scene_maker.operators.show_preferences import OT_ShowPreferences
from addons.scene_maker.operators.initialize_plugin import OT_InitializePlugin
from addons.scene_maker.operators.render_scene_op import OT_RenderScene
from addons.scene_maker.operators.update_asset import OT_UpdateAsset
from addons.scene_maker.operators.align_nodes import OT_AlignNodes
from addons.scene_maker.operators.message_box import OT_MessageBox
from addons.scene_maker.operators.run_script import OT_RunScript

from addons.scene_maker.panels.scene_maker_panels import PT_SceneMakerPanel

from addons.scene_maker.preference.scene_maker_preference import SceneMakerPreference
# Add-on info
bl_info = {
    "name": "Scene Maker",
    "author": "ez",
    "blender": (4, 2, 0),
    "version": (0, 0, 1),
    "description": "The plugin to make scene quickly",
    "warning": "",
    # "doc_url": "[documentation url]",
    # "tracker_url": "[contact email]",
    "support": "COMMUNITY",
    "category": "3D View"
}

CLASSES_BEFORE = [
    SceneMakerAddonProperties
]

CLASSES = [
    OT_GenerateJson,
    OT_ShowPreferences,
    OT_InitializePlugin,
    OT_RenderScene,
    OT_UpdateAsset,
    OT_AlignNodes,
    OT_MessageBox,
    OT_RunScript,

    PT_SceneMakerPanel,
    SceneMakerPreference
]

dir_name_ = Path((os.path.dirname(__file__)))
for pths in dir_name_.parents:
    if str(pths).endswith("scene_maker"):
        dir_name_ = pths
# better_fbx_path = os.path.join(dir_name_, "better_fbx-5.4.19.zip")
template_path = os.path.join(dir_name_, "scene_maker_template.zip")
append_addon_path = os.path.join(dir_name_, "append_addons")

def delayed_execution():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    override = {
                        'area': area, 
                        'region': region
                    }
                    override['selected_objects'] = bpy.context.view_layer.objects[:]
                    override['selected_ids'] = bpy.context.view_layer.objects[:]
                    override['selected_editable_objects'] = bpy.context.view_layer.objects[:]
                    with bpy.context.temp_override(**override):
                        # if 'better_fbx' not in bpy.context.preferences.addons:
                        #     bpy.ops.preferences.addon_install(overwrite=False, enable_on_install=False, filepath=better_fbx_path, filter_folder=True, filter_python=True, filter_glob='*.py;*.zip')
                        #     bpy.ops.preferences.addon_enable(module='better_fbx')

                        # # Check if the script directory is already added
                        # if append_addon_path not in bpy.utils.script_paths():
                        #     bpy.ops.preferences.script_directory_add(directory=append_addon_path, filter_folder=True)

                        # Check if the template is already installed
                        # if 'Browser' not in [template.name for template in bpy.data.screens]:
                        bpy.ops.preferences.app_template_install(overwrite=True, filepath=template_path, filter_folder=True, filter_glob='*.zip')
                        bpy.ops.scene_maker.show_preferences()
    bpy.ops.wm.read_homefile(app_template="scene_maker_template")
    return None

# TODO: Auto create portable folder
def register():
    print("registering")
    bpy.app.timers.register(delayed_execution, first_interval=0)
    for cls in CLASSES_BEFORE:
        bpy.utils.register_class(cls)
    bpy.types.Scene.scene_maker = bpy.props.PointerProperty(type=SceneMakerAddonProperties)
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    
    print("{} addon is installed.".format(bl_info["name"]))


def unregister():
    # Internationalization
    bpy.app.translations.unregister(__addon_name__)
    for cls in CLASSES_BEFORE:
        bpy.utils.unregister_class(cls)
    for cls in CLASSES:
        bpy.utils.unregister_class(cls)

    print("{} addon is uninstalled.".format(bl_info["name"]))
