import os
import bpy

def clear_asset_libraries():
    asset_libraries = bpy.context.preferences.filepaths.asset_libraries

    while asset_libraries:
        asset_libraries.remove(asset_libraries[0])
    print("Asset libraries cleared.")

def clear_script_directories():
    script_directories = bpy.context.preferences.filepaths.script_directories

    while script_directories:
        script_directories.remove(script_directories[0])
    print("Script directories cleared.")
