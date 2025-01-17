import bpy


def clear_animations():
    for obj in bpy.data.objects:
        if obj.animation_data:
            obj.animation_data_clear()


def clean_up_scene():
    if len(bpy.data.materials) > 0:
        for material in bpy.data.materials:
            if material.name == "ImageMaterial":
                bpy.data.materials.remove(material)
            else:
                break

    # while len(bpy.data.meshes) > 0:
    #     bpy.data.meshes.remove(bpy.data.meshes[0])

    # while len(bpy.data.objects) > 0:
    #     bpy.data.objects.remove(bpy.data.objects[0])

    # while len(bpy.data.actions) > 0:
    #     bpy.data.actions.remove(bpy.data.actions[0])

    while len(bpy.data.armatures) > 0:
        bpy.data.armatures.remove(bpy.data.armatures[0])

    while len(bpy.data.curves) > 0:
        bpy.data.curves.remove(bpy.data.curves[0])


def clean_collection(collection_index):
    scene_collection = bpy.context.scene.collection

    if collection_index < 0 or collection_index >= len(scene_collection.children):
        print("无效的集合索引")
        return

    collection_to_clean = scene_collection.children[collection_index]
