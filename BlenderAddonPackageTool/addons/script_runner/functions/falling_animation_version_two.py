import bpy
import re
from mathutils import Vector
from addons.script_runner.functions.import_image import import_image
from addons.script_runner.functions.clear_scene import clear_animations, clean_up_scene
from addons.script_runner.functions.fade_in import fade_in


def falling_animation_version_two():
    clear_animations()
    clean_up_scene()
    diffusion_plane = bpy.data.objects.get("diffusion_image")

    if diffusion_plane is None:
        diffusion_plane = import_image(
            "F:\\mdl-browser-dev\\blender_kits\\assets\\250116\\diffusion_img.png"
        )
        diffusion_plane.name = "diffusion_image"
    floor = bpy.data.objects.get("floor_0")
    if floor is not None:
        # 计算 floor 的包围盒大小
        floor_bbox_corners = [
            floor.matrix_world @ Vector(corner) for corner in floor.bound_box
        ]
        floor_width = max(corner.x for corner in floor_bbox_corners) - min(
            corner.x for corner in floor_bbox_corners
        )
        floor_depth = max(corner.y for corner in floor_bbox_corners) - min(
            corner.y for corner in floor_bbox_corners
        )

        # 设置 diffusion_plane 的缩放
        diffusion_plane.scale.x = floor_width / diffusion_plane.dimensions.x
        diffusion_plane.scale.y = floor_depth / diffusion_plane.dimensions.y

    # 获取所有匹配的对象
    root_objects = [
        obj for obj in bpy.data.objects if obj.type == "MESH" and obj.parent is None
    ]

    frame_start = 0
    frame_end = 30
    for obj in root_objects:
        process_object_hierarchy(obj, frame_start, frame_end)


def process_object_hierarchy(obj, frame_start, frame_end):
    # 先处理当前物体
    if if_match_name_pattern(obj):
        for child in obj.children:
            process_object_hierarchy(child, frame_start, frame_end)
    else:
        raise_obj_bounding_box_to_plane(obj, frame_start, frame_end)
        fade_in(obj, (frame_start, frame_end))

        child_frame_start = frame_end
        child_frame_end = frame_end + 15
        for child in obj.children:
            process_object_hierarchy(child, child_frame_start, child_frame_end)


def raise_obj_bounding_box_to_plane(obj, frame_start, frame_end):
    diffusion_plane = bpy.data.objects.get("diffusion_image")
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    bbox_bottom_z = min(corner.z for corner in bbox_corners)
    diffusion_plane_height = diffusion_plane.location.z
    new_z_position = diffusion_plane_height + (bbox_bottom_z - bbox_bottom_z)
    obj.keyframe_insert(data_path="location", frame=frame_end, index=-1)

    obj.location.z += new_z_position - bbox_bottom_z
    obj.keyframe_insert(data_path="location", frame=frame_start, index=-1)

    fcurves = obj.animation_data.action.fcurves
    for fcurve in fcurves:
        for keyframe in fcurve.keyframe_points:
            if keyframe.co[0] == frame_end:
                keyframe.interpolation = "BEZIER"
                keyframe.handle_left_type = "AUTO"
                keyframe.handle_right_type = "AUTO"


def clear_animations():
    for obj in bpy.data.objects:
        if obj.animation_data:
            obj.animation_data_clear()


def if_match_name_pattern(obj):
    pattern = re.compile(r"^(wall|floor)_[0-9]+$")

    if pattern.match(obj.name) or "diffusion_image" in obj.name:
        return True

    return False
