import bpy
def clear_animations():
    for obj in bpy.data.objects:
        if obj.animation_data:
            obj.animation_data_clear()


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


def fade_in(obj, keyframe):
    bpy.context.view_layer.objects.active = obj
    obj = bpy.context.active_object

    # 在动画开始前将物体的可见性设为不可见
    obj.hide_viewport = True
    obj.hide_render = True

    for slot in obj.material_slots:
        if slot.material:
            old_material = slot.material
            material = old_material.copy()
            slot.material = material
            material.blend_method = "BLEND"
            nodes = material.node_tree.nodes
            links = material.node_tree.links

            output_node = None
            for node in nodes:
                if node.type == "OUTPUT_MATERIAL":
                    output_node = node
                    break

            mix_shader_node = nodes.new(type="ShaderNodeMixShader")
            last_node = get_last_node(material.node_tree)

            links.new(last_node.outputs[0], mix_shader_node.inputs[1])

            transparent_node = nodes.new(type="ShaderNodeBsdfTransparent")
            transparent_node.location = (
                last_node.location.x,
                last_node.location.y + 300,
            )
            links.new(transparent_node.outputs[0], mix_shader_node.inputs[2])
            links.new(mix_shader_node.outputs[0], output_node.inputs[0])
            output_node.location = (
                mix_shader_node.location.x + 200,
                mix_shader_node.location.y,
            )

            bpy.context.scene.frame_set(keyframe[0])
            mix_shader_node.inputs["Fac"].default_value = 1.0
            mix_shader_node.inputs["Fac"].keyframe_insert(
                data_path="default_value", frame=keyframe[0]
            )
            bpy.context.scene.frame_set(keyframe[1])
            mix_shader_node.inputs["Fac"].default_value = 0.0
            mix_shader_node.inputs["Fac"].keyframe_insert(
                data_path="default_value", frame=keyframe[1]
            )

    obj.hide_viewport = True
    obj.hide_render = True
    obj.keyframe_insert(data_path="hide_viewport", frame=keyframe[0]-1)
    obj.keyframe_insert(data_path="hide_render", frame=keyframe[0]-1)

    obj.hide_viewport = False
    obj.hide_render = False
    obj.keyframe_insert(data_path="hide_viewport", frame=keyframe[0])
    obj.keyframe_insert(data_path="hide_render", frame=keyframe[0])


def get_last_node(node_tree):
    nodes = node_tree.nodes
    last_node = None
    max_x = -float("inf")
    for node in nodes:
        if node.location.x > max_x and node.type != "OUTPUT_MATERIAL":
            max_x = node.location.x
            last_node = node
    return last_node

