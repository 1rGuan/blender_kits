import os
import bpy
import time


def save_previous_settings(scene, additional_info=None):
    previous_settings = {
        "workspace": bpy.context.window.workspace,
        "render_engine": scene.render.engine,
        "color_depth": scene.render.image_settings.color_depth,
        "compression": scene.render.image_settings.compression,
        "display_device": scene.display_settings.display_device,
        "shading_color_type": None,
        "view_transform": scene.view_settings.view_transform,
    }

    if scene.render.engine == "BLENDER_WORKBENCH":
        previous_settings["shading_color_type"] = scene.display.shading.color_type
        previous_settings["shading_light"] = scene.display.shading.light

    if additional_info:
        previous_settings.update(additional_info)

    return previous_settings


def restore_previous_settings(scene, previous_settings):
    scene.render.engine = previous_settings["render_engine"]
    scene.render.image_settings.color_depth = previous_settings["color_depth"]
    scene.render.image_settings.compression = previous_settings["compression"]
    scene.display_settings.display_device = previous_settings["display_device"]
    scene.view_settings.view_transform = previous_settings["view_transform"]
    bpy.context.window.workspace = previous_settings["workspace"]

    if previous_settings["shading_color_type"] is not None:
        scene.display.shading.color_type = previous_settings["shading_color_type"]
        scene.display.shading.light = previous_settings["shading_light"]


def render_scene(scene_name, output_path, render_camera):
    print("Render scene")
    scene = bpy.context.scene
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = "PNG"
    previous_settings = save_previous_settings(scene)
    if render_camera:
        render_shading_path = os.path.join(output_path, f"{scene_name}_shading.png")
        render_depth_path = os.path.join(output_path, f"{scene_name}_depth.png")
        render_seg_path = os.path.join(output_path, f"{scene_name}_seg.png")
        render_shading_map(render_camera, render_shading_path)
        render_depth_map(render_camera, render_depth_path)
        render_seg_map(render_camera, render_seg_path)

    restore_previous_settings(scene, previous_settings)


def render_shading_map(camera_obj, output_path):
    print("Render Shading map")
    scene = bpy.context.scene
    previous_settings = save_previous_settings(scene)

    scene.use_nodes = False
    scene.render.filepath = output_path

    render_camera_obj = bpy.data.objects.get(camera_obj)
    scene.render.engine = "BLENDER_EEVEE_NEXT"

    scene.camera = render_camera_obj
    bpy.ops.render.render(write_still=True)

    # restore_previous_settings(scene, previous_settings)


def render_depth_map(camera_obj, output_path):
    print("Render Depth map")
    scene = bpy.context.scene
    scene.render.filepath = output_path

    previous_settings = save_previous_settings(scene)

    bpy.context.window.workspace = bpy.data.workspaces.get("Compositing")
    scene.use_nodes = True
    scene.view_layers["ViewLayer"].use_pass_z = True
    time.sleep(0.1)

    if scene.node_tree is None:
        scene.node_tree = bpy.data.node_groups.new(
            "CompositorNodeTree", "CompositorNodeTree"
        )
    nodes = scene.node_tree.nodes
    links = scene.node_tree.links

    for node in nodes:
        nodes.remove(node)

    input_node = nodes.new(type="CompositorNodeRLayers")
    input_node.location = (-400, 0)

    output_node = nodes.new(type="CompositorNodeComposite")
    output_node.location = (800, 0)

    normalize_node = nodes.new(type="CompositorNodeNormalize")
    normalize_node.location = (0, 0)

    invert_node = nodes.new(type="CompositorNodeInvert")
    invert_node.location = (400, 0)

    links.new(input_node.outputs["Depth"], normalize_node.inputs["Value"])
    links.new(normalize_node.outputs["Value"], invert_node.inputs["Color"])
    links.new(invert_node.outputs["Color"], output_node.inputs["Image"])

    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.image_settings.color_depth = "16"
    scene.render.image_settings.compression = 0
    scene.display.shading.color_type = "OBJECT"
    scene.display_settings.display_device = "Display P3"
    scene.view_settings.view_transform = "Raw"

    render_camera_obj = bpy.data.objects.get(camera_obj)
    scene.camera = render_camera_obj
    bpy.ops.render.render(write_still=True)
    scene.use_nodes = False

    restore_previous_settings(scene, previous_settings)


def render_seg_map(camera_obj, output_path):
    print("Render Segment map")
    scene = bpy.context.scene
    scene.render.filepath = output_path

    previous_settings = save_previous_settings(scene)

    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.image_settings.color_depth = "16"
    scene.render.image_settings.compression = 0
    scene.display.shading.color_type = "RANDOM"
    scene.display.shading.light = "FLAT"

    render_camera_obj = bpy.data.objects.get(camera_obj)
    scene.camera = render_camera_obj
    bpy.ops.render.render(write_still=True)

    restore_previous_settings(scene, previous_settings)
