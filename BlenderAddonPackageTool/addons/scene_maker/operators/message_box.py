import bpy

class OT_MessageBox(bpy.types.Operator):
    bl_idname = "scene_maker.message_box"
    bl_label = "Simple Message Box"
    
    message = bpy.props.StringProperty()

    def draw(self, context):
        layout = self.layout
        layout.label(text=self.message)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        return {'FINISHED'}
