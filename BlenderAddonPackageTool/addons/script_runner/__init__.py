import os
import bpy
from pathlib import Path

from addons.script_runner.config import __addon_name__

from addons.script_runner.properties import ScriptRunnerProperties

from addons.script_runner.panels.ScriptRunnerPanel import PT_ScriptRunner
from addons.script_runner.operators.FallingAnimationOperator import OT_FallingAnimation
from addons.script_runner.operators.FallingAnimationOperatorV2 import OT_FallingAnimationVersionTwo
# from addons.script_runner.operators.FallingAnimationOperator import OT_FallingAnimation

# Add-on info
bl_info = {
    "name": "Script Runner",
    "author": "ez",
    "blender": (4, 2, 0),
    "version": (0, 0, 1),
    "description": "The plugin to run scripts quickly",
    "warning": "",
    # "doc_url": "[documentation url]",
    # "tracker_url": "[contact email]",
    "support": "COMMUNITY",
    "category": "3D View"
}

CLASSES_BEFORE = [
    ScriptRunnerProperties
]
#
CLASSES = [
    OT_FallingAnimation,
    OT_FallingAnimationVersionTwo,
    PT_ScriptRunner,
]

dir_name_ = Path((os.path.dirname(__file__)))
for pths in dir_name_.parents:
    if str(pths).endswith("script_runner"):
        dir_name_ = pths
# better_fbx_path = os.path.join(dir_name_, "better_fbx-5.4.19.zip")
# template_path = os.path.join(dir_name_, "scene_maker_template.zip")
# append_addon_path = os.path.join(dir_name_, "append_addons")

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
    #                 with bpy.context.temp_override(**override):
    #                     if 'better_fbx' not in bpy.context.preferences.addons:
    #                         bpy.ops.preferences.addon_install(overwrite=False, enable_on_install=False, filepath=better_fbx_path, filter_folder=True, filter_python=True, filter_glob='*.py;*.zip')
    #                         bpy.ops.preferences.addon_enable(module='better_fbx')
    #
    #                     # Check if the script directory is already added
    #                     if append_addon_path not in bpy.utils.script_paths():
    #                         bpy.ops.preferences.script_directory_add(directory=append_addon_path, filter_folder=True)
    #
    #                     Check if the template is already installed
    #                     if 'Browser' not in [template.name for template in bpy.data.screens]:
    #                     bpy.ops.preferences.app_template_install(overwrite=True, filepath=template_path, filter_folder=True, filter_glob='*.zip')
    #                     bpy.ops.scene_maker.show_preferences()
    # bpy.ops.wm.read_homefile(app_template="scene_maker_template")
    return None

# TODO: Auto create portable folder
def register():
    print("registering")
    bpy.app.timers.register(delayed_execution, first_interval=0)
    for cls in CLASSES_BEFORE:
        bpy.utils.register_class(cls)
    bpy.types.Scene.script_runner = bpy.props.PointerProperty(type=ScriptRunnerProperties)
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
