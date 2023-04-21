bl_info = {
    "name": "Mirror Multiple Objects",
    "blender": (2, 80, 0),
    "category": "Object",
    "version": (1, 4, 1),
    "author": "kreby",
    "description": "mirrors all selected objects over active object",
}

import bpy

class MyProperties(bpy.types.PropertyGroup):
    PROPS = [
        ('mirrorX', bpy.props.BoolProperty(name='X', default=False)),
        ('mirrorY', bpy.props.BoolProperty(name='Y', default=False)),
        ('mirrorZ', bpy.props.BoolProperty(name='Z', default=False)),
    ]

    symm_obj_options = [
            ('OP1', '3D Cursor', '', 0),
            ('OP2', 'Active Obj. Origin', '', 1)
    ]

    num_copies : bpy.props.IntProperty(
        name="Num. of Copies", 
        description="how many copies", 
        default=2, 
        min=2,
        max=360,
        step=1, 
    )

    symm_obj : bpy.props.EnumProperty(  # holds the point at which the objects will be rotated around, either 3d cursor or obj's origin
        name="Rotation Origin",
        description="what to rotate around",
        default=0,
        items=symm_obj_options, # ~ MAKE FLAG VERSION ~
    )

# ~~ OPERATORs
class RemoveMirrorMult(bpy.types.Operator):
    bl_idname = "object.remove_mirror_mult"
    bl_label = "Unmirror Selected Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):        
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
            scene.mirrorX,
            scene.mirrorY,
            scene.mirrorZ,
        )
        
        target_obj = context.active_object    # makes the active object the "target"
        tool_objs = [o for o in context.selected_objects if o != target_obj]    # makes every other object applicable to the mirror

        for obj in tool_objs:
            obj.modifiers.new(pref, type='MIRROR')    # creates a mirror modifier with an appropriate name
            
            #try obj.modif
            obj.modifiers[len(obj.modifiers)-1].mirror_object = target_obj  # sets the mirror object to the active object
            obj.modifiers[len(obj.modifiers)-1].use_axis = params  # sets appropriate mirror axes
            
            
        # the code to mirror multiple objects
        
        return {'FINISHED'}

class RotationalSymmetryOperator(bpy.types.Operator):
    bl_idname = "object.rotate_sym"
    bl_label = "Rotationally Symmetrize"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        
        num_items = mytool.num_copies
        
        cursor_loc = scene.cursor.location

        if mytool.symm_obj == 'OP1':
            tool_objs = context.selected_objects
        if mytool.symm_obj == 'OP2':
            cursor_loc = scene.cursor.location # holds the past location of the cursor
            target_obj = context.active_object
            
            empty_dims = target_obj.dimensions # used to calculate the largest dimension so that the empty object used to mirror is easily visible
            empty_dims_list = [empty_dims.x, empty_dims.y, empty_dims.z]
            empty_radius = max(empty_dims_list)

            tool_objs = [o for o in context.selected_objects if o != target_obj]

            scene.cursor.location = target_obj.location
        
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=scene.cursor.location, radius=(empty_radius*1.1))

        for obj in tool_objs:
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            

        # add empty

        scene.cursor.location = cursor_loc
    
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
        for (prop_name, _) in MyProperties.PROPS:
            row.prop(context.scene, prop_name)
            
        row = self.layout.row(align=False) 
        row.operator(MirrorObjectsOperator.bl_idname, text=MirrorObjectsOperator.bl_label)

        row = self.layout.row(align=False) 
        row.operator(RemoveMirrorMult.bl_idname, text=RemoveMirrorMult.bl_label)

class RotateSymmPanel(bpy.types.Panel):
    bl_category = 'kreby'
    bl_idname = 'VIEW3D_PT_rotate_symmetry'
    bl_label = 'Rotational Symmetry'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool # allows for reference of MyProperties

        layout.prop(mytool, "num_copies")
        layout.prop(mytool, "symm_obj")

        layout.operator(RotationalSymmetryOperator.bl_idname, text=RotationalSymmetryOperator.bl_label)

# ~~ ROUTINE
CLASSES = [ # all classes that are used within the operators and panels
    MyProperties,
    RemoveMirrorMult,
    MirrorObjectsOperator,
    MirrorObjectsPanel,
    RotationalSymmetryOperator,
    RotateSymmPanel
]

def register():
    for klass in CLASSES:
        bpy.utils.register_class(klass)

        bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyProperties) # creates my_tool (the property group reference) in each class being registered

    for (prop_name, prop_value) in MyProperties.PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)

def unregister():
    for (prop_name, _) in MyProperties.PROPS:
        delattr(bpy.types.Scene, prop_name)

    for klass in CLASSES:
        bpy.utils.unregister_class(klass)

        del bpy.types.Scene.my_tool # deletes the reference
        

if __name__ == '__main__':
    register()