import bpy

def get_camera_items(self, context):
    cameras = [cam.name for cam in bpy.data.cameras]
    items = [("", "No camera", "Choose a camera from the list")]
    items.extend([(cam, cam, "") for cam in cameras])
    
    return [(cam, cam, "") for cam in cameras]

def update_scene_name(self, context):
    bpy.context.scene.scene_maker.scene_name_suffix = 0

class ScriptRunnerProperties(bpy.types.PropertyGroup):
    asset_path: bpy.props.StringProperty(name="Asset Path", default="", subtype="DIR_PATH", description="资产存储路径") # type: ignore
