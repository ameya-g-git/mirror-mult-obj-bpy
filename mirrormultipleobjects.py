bl_info = {
    "name": "Mirror Multiple Objects",
    "blender": (2, 80, 0),
    "category": "Object",
    "version": (1, 3, 1),
    "author": "kreby",
    "description": "mirrors all selected objects over active object",
}

import bpy

PROPS = [
    ('mirrorX', bpy.props.BoolProperty(name='X', default=False)),
    ('mirrorY', bpy.props.BoolProperty(name='Y', default=False)),
    ('mirrorZ', bpy.props.BoolProperty(name='Z', default=False)),
]

# ~~ OPERATORs
class RemoveMirrorMult(bpy.types.Operator):
    bl_idname = "object.remove_mirror_mult"
    bl_label = "Unmirror Selected Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        
        selected = context.selected_objects

        for obj in selected:
            mirrorMultMods = [mod for mod in obj.modifiers if mod.name[:10] == "MirrorMult"]
            if mirrorMultMods:
                obj.modifiers.remove(mirrorMultMods[-1])
        
        return {'FINISHED'}

class MirrorObjectsOperator(bpy.types.Operator):
    bl_idname = "object.mirror_mult"
    bl_label = "Mirror Selected Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        pref = "MirrorMult" # name preference
        
        params = (
            context.scene.mirrorX,
            context.scene.mirrorY,
            context.scene.mirrorZ,
        )
        
        (mirrorX, mirrorY, mirrorZ) = params
        
        axes_used = (mirrorX, mirrorY, mirrorZ)
        
        
        target_obj = context.active_object    # makes the active object the "target"
        tool_objs = [o for o in context.selected_objects if o != target_obj]    # makes every other object applicable to the mirror

        for obj in tool_objs:
            mirMult = obj.modifiers.new(pref, type='MIRROR')    # creates a mirror modifier with an appropriate name
            
            #try obj.modif
            obj.modifiers[len(obj.modifiers)-1].mirror_object = target_obj  # sets the mirror object to the active object
            obj.modifiers[len(obj.modifiers)-1].use_axis = axes_used  # sets the mirror object to the active object
            
            
        # the code to mirror multiple objects
        
        return {'FINISHED'}

# ~~ PANEL

class MirrorObjectsPanel(bpy.types.Panel):
    bl_category = 'kreby'
    bl_idname = 'VIEW3D_PT_mirror_multiple'
    bl_label = 'Mirror Multiple Objects'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context):
        self.layout.label(text='Mirror Axes')
        row = self.layout.row(align=True)
        for (prop_name, _) in PROPS:
            row.prop(context.scene, prop_name)
            
        row = self.layout.row(align=False) 
        row.operator(MirrorObjectsOperator.bl_idname, text='Mirror Selected Objects')

        row = self.layout.row(align=False) 
        row.operator('object.remove_mirror_mult', text='Unmirror Selected Objects')

# ~~ ROUTINE
CLASSES = [
    RemoveMirrorMult,
    MirrorObjectsOperator,
    MirrorObjectsPanel,
]

def register():
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
    
    for klass in CLASSES:
        bpy.utils.register_class(klass)

def unregister():
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)

    for klass in CLASSES:
        bpy.utils.unregister_class(klass)
        

if __name__ == '__main__':
    register()