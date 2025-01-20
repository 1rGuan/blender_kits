import bpy
import mathutils
import math


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


def create_bounding_box_cube(min_corner, max_corner):
    center = (min_corner + max_corner) / 2
    size = max_corner - min_corner

    bpy.ops.mesh.primitive_cube_add(size=2, location=center)
    cube = bpy.context.object

    cube.scale = size / 2
    cube.name = "scene_bbx"

    return cube


def create_camera_and_path(target_obj, center, radius):
    bpy.ops.object.camera_add(location=(0, 0, 0))
    camera = bpy.context.object
    camera.name = "rotating_camera"

    adjust_camera_to_fit_object(camera, target_obj)

    camera_distance = (camera.location - center).length

    bpy.ops.curve.primitive_bezier_circle_add(radius=camera_distance, location=center)
    path = bpy.context.object

    constraint = camera.constraints.new(type="FOLLOW_PATH")
    constraint.target = path
    constraint.use_curve_follow = True

    constraint = camera.constraints.new(type="TRACK_TO")
    constraint.target = target_obj
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"
    return camera, path


def adjust_camera_to_fit_object(camera, obj):
    # 计算物体的边界框
    bbox_corners = [
        obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box
    ]

    # 计算边界框的中心和大小
    bbox_center = sum(bbox_corners, mathutils.Vector()) / 8
    bbox_size = max((corner - bbox_center).length for corner in bbox_corners)

    # 设置相机位置
    camera_distance = bbox_size / math.tan(camera.data.angle / 2)
    camera_vector = camera.location - bbox_center
    camera_vector.normalize()
    camera.location = (
        bbox_center + camera_vector * camera_distance * 1.1
    )  # 稍微往后移动一点

    # 让相机看向物体中心
    direction = bbox_center - camera.location
    rot_quat = direction.to_track_quat("-Z", "Y")
    camera.rotation_euler = rot_quat.to_euler()


def main():
    scene_min, scene_max = calculate_scene_bounding_box()
    cube = create_bounding_box_cube(scene_min, scene_max)
    center = (scene_min + scene_max) / 2
    radius = max((scene_max - scene_min).length / 2, 1)
    camera, path = create_camera_and_path(cube, center, radius)
    camera.location = (0, 0, 0)
    # adjust_camera_to_fit_object(camera, cube)
    cube.hide_viewport = True
    cube.hide_render = True

    # 设置相机为活动相机
    bpy.context.scene.camera = camera