import bpy
from addons.script_runner.functions.fade_in import fade_in

item_dict = {
    "item1": (0, 30),
    "item2": (0, 30),
    "item3": (30, 60)
}

def transparentfade_in_by_name_by_name(item_dict):
    for item_name, keyframes in item_dict.items():
        fade_in(item_name, keyframes)
