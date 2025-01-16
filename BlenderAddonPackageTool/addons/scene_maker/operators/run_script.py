import bpy


class OT_RunScript(bpy.types.Operator):
    bl_idname = "scene_maker.run_script"
    bl_label = "Run Script"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        scene = bpy.context.scene
        script_path = scene.scene_maker.script_path
        
        if not script_path:
            print("Script path is not set.")
            return {'CANCELLED'}
        
        try:
            with open(script_path, 'r') as file:
                script_content = file.read()

            exec(script_content, globals(), locals())
            print(f"Executed script: {script_path}")
            return {'FINISHED'}
        except Exception as e:
            print(f"Failed to execute script: {script_path}")
            print(f"Error: {e}")
            return {'CANCELLED'}
