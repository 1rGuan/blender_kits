import bpy


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
            material.surface_render_method = "DITHERED"
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
    obj.keyframe_insert(data_path="hide_viewport", frame=keyframe[0] - 1)
    obj.keyframe_insert(data_path="hide_render", frame=keyframe[0] - 1)

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
