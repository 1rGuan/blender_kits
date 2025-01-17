import bpy


def import_image(image_path):
    # 创建一个新的平面
    bpy.ops.mesh.primitive_plane_add(
        size=1, enter_editmode=False, align="WORLD", location=(0, 0, 0)
    )
    plane = bpy.context.object  # 获取新创建的平面对象

    # 加载图片
    img = bpy.data.images.load(image_path)

    # 创建一个新的材质
    material = bpy.data.materials.new(name="ImageMaterial")
    material.use_nodes = True  # 使用节点

    # 获取材质的节点树
    nodes = material.node_tree.nodes
    nodes.clear()  # 清空默认节点

    # 创建纹理节点
    texture_node = nodes.new(type="ShaderNodeTexImage")
    texture_node.image = img

    emission_node = nodes.new(type="ShaderNodeEmission")

    # 创建输出节点
    output_node = nodes.new(type="ShaderNodeOutputMaterial")

    # 连接节点
    links = material.node_tree.links
    links.new(texture_node.outputs["Color"], emission_node.inputs["Color"])
    links.new(emission_node.outputs["Emission"], output_node.inputs["Surface"])

    # 将材质赋给平面
    if plane.data.materials:
        plane.data.materials[0] = material
    else:
        plane.data.materials.append(material)

    # 设置平面的比例以匹配图片的比例
    aspect_ratio = img.size[0] / img.size[1]
    plane.scale[0] = aspect_ratio  # X轴缩放
    plane.scale[1] = 1.0  # Y轴保持为1.0

    return plane
