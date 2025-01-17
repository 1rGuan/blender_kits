import bpy
import re
import random
import mathutils
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
            "D:\\BlenderScript\\blender_kits\\assets\\250116\\diffusion_img.png"
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

    scene_bbx = bpy.data.objects.get("scene_bbx")
    if scene_bbx is None:
        scene_min, scene_max = calculate_scene_bounding_box()
        scene_bbx = create_bounding_box_cube(scene_min, scene_max)
    
    diffusion_plane.location.z += scene_bbx.dimensions.z * 3 + diffusion_plane.dimensions.z


    # 获取所有匹配的对象
    root_objects = [
        obj for obj in bpy.data.objects if obj.type == "MESH" and obj.parent is None and obj.name!="scene_bbx"
    ]

    frame_start = 0
    frame_end = 30
    random_offset = random.randint(0, 20)
    frame_start += random_offset
    frame_end += random_offset
    for obj in root_objects:
        process_object_hierarchy(obj, frame_start, frame_end)
    
    scene_bbx.hide_viewport = True
    scene_bbx.hide_render = True


def process_object_hierarchy(obj, frame_start, frame_end):
    # 先处理当前物体
    if if_match_name_pattern(obj):
        for child in obj.children:
            process_object_hierarchy(child, frame_start, frame_end)
    else:
        # 添加随机时间偏移
        random_offset = random.randint(0, 15)
        frame_start += random_offset+30
        frame_end += random_offset+30

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


def if_match_name_pattern(obj):
    pattern = re.compile(r"^(wall|floor)_[0-9]+$")

    if pattern.match(obj.name) or "diffusion_image" in obj.name:
        return True

    return False

def create_bounding_box_cube(min_corner, max_corner):
    center = (min_corner + max_corner) / 2
    size = max_corner - min_corner

    bpy.ops.mesh.primitive_cube_add(size=2, location=center)
    cube = bpy.context.object

    cube.scale = size / 2
    cube.name = "scene_bbx"

    return cube

def calculate_scene_bounding_box():
    min_corner = mathutils.Vector((float("inf"), float("inf"), float("inf")))
    max_corner = mathutils.Vector((float("-inf"), float("-inf"), float("-inf")))

    for obj in bpy.context.scene.objects:
        if obj.type in {"MESH", "CURVE", "SURFACE", "META", "FONT"}:
            obj_min, obj_max = get_bounding_box(obj)
            min_corner.x = min(min_corner.x, obj_min.x)
            min_corner.y = min(min_corner.y, obj_min.y)
            min_corner.z = min(min_corner.z, obj_min.z)
            max_corner.x = max(max_corner.x, obj_max.x)
            max_corner.y = max(max_corner.y, obj_max.y)
            max_corner.z = max(max_corner.z, obj_max.z)

    return min_corner, max_corner

def get_bounding_box(obj):
    bbox_corners = [
        obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box
    ]
    min_corner = mathutils.Vector(
        (
            min([v.x for v in bbox_corners]),
            min([v.y for v in bbox_corners]),
            min([v.z for v in bbox_corners]),
        )
    )
    max_corner = mathutils.Vector(
        (
            max([v.x for v in bbox_corners]),
            max([v.y for v in bbox_corners]),
            max([v.z for v in bbox_corners]),
        )
    )
    return min_corner, max_corner