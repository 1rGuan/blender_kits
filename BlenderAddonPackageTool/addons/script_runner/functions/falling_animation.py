import bpy
from addons.script_runner.functions.clear_scene import clear_animations
from addons.script_runner.functions.fade_in import fade_in


def falling_animation():
    clear_animations()
    root_objects = [
        obj for obj in bpy.data.objects if obj.type == "MESH" and obj.parent is None
    ]

    # 递归处理每一层的物体
    frame_start = 0
    frame_end = 60
    for root_obj in root_objects:
        process_object_hierarchy(root_obj, frame_start, frame_end)


def process_object_hierarchy(obj, frame_start, frame_end):
    # 如果物体名称中包含 "wall" 或 "floor"，则不处理该物体，但处理其子物体
    if "wall" in obj.name or "floor" in obj.name:
        for child in obj.children:
            process_object_hierarchy(child, frame_start, frame_end)
    else:
        # 处理当前物体
        print(obj.name)
        raise_obj_height(obj, frame_start, frame_end)
        fade_in(obj, (frame_start, frame_end))

        # 处理子物体
        child_frame_start = frame_end
        child_frame_end = frame_end + 60
        for child in obj.children:
            process_object_hierarchy(child, child_frame_start, child_frame_end)


def raise_obj_height(obj, frame_start, frame_end):
    current_location = obj.location.copy()

    bbox_height = obj.dimensions.z

    obj.location.z += bbox_height * 0.5

    obj.keyframe_insert(data_path="location", frame=frame_start, index=-1)

    obj.location = current_location
    obj.keyframe_insert(data_path="location", frame=frame_end, index=-1)

    fcurves = obj.animation_data.action.fcurves
    for fcurve in fcurves:
        for keyframe in fcurve.keyframe_points:
            if keyframe.co[0] == frame_end:
                keyframe.interpolation = "BEZIER"
                keyframe.handle_left_type = "AUTO"
                keyframe.handle_right_type = "AUTO"
