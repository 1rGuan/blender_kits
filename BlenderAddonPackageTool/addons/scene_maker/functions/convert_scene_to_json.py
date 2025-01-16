import bpy
import mathutils
import json

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

    camera_params = {
        "focal_length": float(f"{focal_length:.6f}"),
        "sensor_width": float(f"{sensor_width:.6f}"),
        "sensor_height": float(f"{sensor_height:.6f}"),
        "location": [float(f"{location.x:.6f}"), float(f"{location.y:.6f}"), float(f"{location.z:.6f}")],
        "rotation_euler": [float(f"{rotation.x:.6f}"), float(f"{rotation.y:.6f}"), float(f"{rotation.z:.6f}")],
        "camera_transform_matrix": [[float(f"{value:.6f}") for value in row] for row in camera_transform]
    }

    return camera_params

def get_light_parameters(light_obj):
    light_data = light_obj.data
    location = light_obj.location
    rotation = light_obj.rotation_euler

    light_params = {
        "name": light_obj.name,
        "type": light_data.type,
        "location": [float(f"{location.x:.6f}"), float(f"{location.y:.6f}"), float(f"{location.z:.6f}")],
        "rotation_euler": [float(f"{rotation.x:.6f}"), float(f"{rotation.y:.6f}"), float(f"{rotation.z:.6f}")],
        "energy": float(f"{light_data.energy:.6f}"),
        "color": [float(f"{c:.6f}") for c in light_data.color]
    }

    if light_data.type in {'POINT', 'SUN', 'SPOT'}:
        light_params["distance"] = float(f"{light_data.cutoff_distance:.6f}")

    if light_data.type == 'SPOT':
        light_params["spot_size"] = float(f"{light_data.spot_size:.6f}")
        light_params["spot_blend"] = float(f"{light_data.spot_blend:.6f}")

    return light_params

def is_asset(obj):
    return obj.asset_data is not None

def convert_scene_to_json(scene_name, camera_obj_name):
    scene_data = {}
    scene_data["scene"] = []
    scene_data["lights"] = []

    def process(obj, parent_name=None):
        if obj.type != 'MESH':
            return None

        location = obj.location
        rotation = obj.rotation_euler

        quaternion = rotation.to_quaternion()

        pose_matrix = mathutils.Matrix.Translation(location) @ quaternion.to_matrix().to_4x4()

        bbox_corners = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
        min_point = mathutils.Vector((min(corner.x for corner in bbox_corners),
                            min(corner.y for corner in bbox_corners),
                            min(corner.z for corner in bbox_corners)))
        max_point = mathutils.Vector((max(corner.x for corner in bbox_corners),
                            max(corner.y for corner in bbox_corners),
                            max(corner.z for corner in bbox_corners)))

        obj_data = {
            "name": obj.name,
            "type": obj.type,
            "pose_matrix": [[float(f"{pose_matrix[row][col]:.6f}") for col in range(4)] for row in range(4)],
            "parent_name": parent_name,
            "bounding_box": {
                "min": [float(f"{min_point.x:.6f}"), float(f"{min_point.y:.6f}"), float(f"{min_point.z:.6f}")],
                "max": [float(f"{max_point.x:.6f}"), float(f"{max_point.y:.6f}"), float(f"{max_point.z:.6f}")]
            },
            "child_objects": []
        }

        for child in obj.children:
            child_data = process(child, obj.name)
            if child_data:
                obj_data["child_objects"].append(child_data)
        
        return obj_data

    for obj in bpy.context.scene.objects:
        if not obj.parent and obj.type == 'MESH':
            scene_data["scene"].append(process(obj))
        elif obj.type == 'LIGHT':
            light_params = get_light_parameters(obj)
            scene_data["lights"].append(light_params)

    camera_params = get_camera_parameters(camera_obj_name)
    scene_data["camera"] = camera_params

    json_path = bpy.context.scene.scene_maker.img_output_folder
    
    json_file = json_path + "/" + f"{scene_name}.json"
    save_scene_to_json(scene_data, json_file)

    print("Json Generated")
    return

class CustomJSONEncoder(json.JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, list) and all(isinstance(i, list) for i in obj):
            return '[\n' + ',\n'.join('    ' + json.dumps(row) for row in obj) + '\n]'
        elif isinstance(obj, list):
            return '[' + ', '.join(json.dumps(i) for i in obj) + ']'
        return json.JSONEncoder.encode(self, obj)

    def iterencode(self, obj, _one_shot=False):
        if isinstance(obj, list) and all(isinstance(i, list) for i in obj):
            return ('[\n' + ',\n'.join('    ' + json.dumps(row) for row in obj) + '\n]').splitlines(True)
        elif isinstance(obj, list):
            return ('[' + ', '.join(json.dumps(i) for i in obj) + ']').splitlines(True)
        return super().iterencode(obj, _one_shot)

def save_scene_to_json(scene_data, json_file):
    with open(json_file, 'w') as f:
        # json.dump(scene_data, f, indent=4, cls=CustomJSONEncoder)
        json.dump(scene_data, f, indent=4)
