import bpy

def get_camera_items(self, context):
    cameras = [cam.name for cam in bpy.data.cameras]
    items = [("", "No camera", "Choose a camera from the list")]
    items.extend([(cam, cam, "") for cam in cameras])
    
    return [(cam, cam, "") for cam in cameras]

def update_scene_name(self, context):
    bpy.context.scene.scene_maker.scene_name_suffix = 0

class SceneMakerAddonProperties(bpy.types.PropertyGroup):
    # author_name: bpy.props.StringProperty(name="Author Name", default="ezguan", description="作者名称")  # type: ignore
    # asset_path: bpy.props.StringProperty(name="Asset Path", default="W:/aispace/scene_asset", subtype="DIR_PATH", description="资产存储路径") # type: ignore
    # json_path: bpy.props.StringProperty(name="JSON Path", default="W:/aispace/results", subtype="DIR_PATH", description="场景数据导出路径") # type: ignore
    # img_output_folder: bpy.props.StringProperty(name="Image Path", default="W:/aispace/results", subtype="DIR_PATH", description="渲染结果保存路径") # type: ignore

    # scene_name: bpy.props.StringProperty(name="Scene Name", default="scene", description="场景名称", update=update_scene_name) # type: ignore
    # scene_name_suffix: bpy.props.IntProperty(name='Scene Name Suffix', default=0, description='场景名自动后缀')  # type: ignore
    # render_camera: bpy.props.EnumProperty(name="Render Camera", description="选择一个相机", items=get_camera_items) # type: ignore
    # margin: bpy.props.IntProperty(name='Margin', default=50, description='The amount of space between nodes')  # type: ignore


    author_name: bpy.props.StringProperty(name="Author Name", default="", description="作者名称")  # type: ignore
    asset_path: bpy.props.StringProperty(name="Asset Path", default="", subtype="DIR_PATH", description="资产存储路径") # type: ignore
    json_path: bpy.props.StringProperty(name="JSON Path", default="", subtype="DIR_PATH", description="场景数据导出路径") # type: ignore
    img_output_folder: bpy.props.StringProperty(name="Image Path", default="", subtype="DIR_PATH", description="渲染结果保存路径") # type: ignore

    scene_name: bpy.props.StringProperty(name="Scene Name", default="", description="场景名称", update=update_scene_name) # type: ignore
    scene_name_suffix: bpy.props.IntProperty(name='Scene Name Suffix', default=0, description='场景名自动后缀')  # type: ignore
    render_camera: bpy.props.EnumProperty(name="Render Camera", description="选择一个相机", items=get_camera_items) # type: ignore
    margin: bpy.props.IntProperty(name='Margin', default=50, description='The amount of space between nodes')  # type: ignore
    script_path: bpy.props.StringProperty(name="Script Path", default="", subtype="FILE_PATH", description="执行脚本路径") # type: ignore
