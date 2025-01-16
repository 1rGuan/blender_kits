import os
import bpy
from addons.scene_maker.functions.clear_asset_and_script_path import clear_asset_libraries

def add_asset_libraries():
    assets_path = bpy.context.scene.scene_maker.asset_path
    if assets_path == "":
        print("No asset path")
        return
    else:
        clear_asset_libraries()

        for folder in os.listdir(assets_path):
            folder_path = os.path.join(assets_path, folder)
            if os.path.isdir(folder_path):
                bpy.ops.preferences.asset_library_add(directory=folder_path)
                print(f"Added asset library: {folder_path}")

    bpy.ops.script.reload()
