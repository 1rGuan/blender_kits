import bpy
import mathutils

def get_camera_parameters(camera_obj):
    camera_obj = bpy.context.scene.objects[camera_obj]
    if camera_obj.type != 'CAMERA':
        raise ValueError("The provided object is not a camera.")

    focal_length = camera_obj.data.lens
    sensor_width = camera_obj.data.sensor_width
    sensor_height = camera_obj.data.sensor_height

    location = camera_obj.location
    rotation = camera_obj.rotation_euler

    rotation_matrix = rotation.to_matrix().to_4x4()

    camera_transform = mathutils.Matrix.Translation(location) @ rotation_matrix

    print("Camera Parameters:")
    print(f"Focal Length: {focal_length}")
    print(f"Sensor Width: {sensor_width}")
    print(f"Sensor Height: {sensor_height}")
    print(f"Location: {location}")
    print(f"Rotation (Euler): {rotation}")
    print(f"Camera Transform Matrix:\n{camera_transform}")

