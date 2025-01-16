import os
import bpy

def clear_all_asset_libraries():
    asset_libraries = bpy.context.preferences.filepaths.asset_libraries
    for i in range(len(asset_libraries)):
        bpy.ops.preferences.asset_library_remove(index=0)
