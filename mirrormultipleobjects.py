bl_info = {
    "name": "Mirror Multiple Objects",
    "blender": (2, 80, 0),
    "category": "Object",
    "version": (2, 1, 1),
    "author": "kreby",
    "description": "mirrors all selected objects over active object",
}

import bpy
from mathutils import Euler
from math import radians

class MyProperties(bpy.types.PropertyGroup):
    PROPS = [
        ('mirrorX', bpy.props.BoolProperty(name='X', default=False)),
        ('mirrorY', bpy.props.BoolProperty(name='Y', default=False)),
        ('mirrorZ', bpy.props.BoolProperty(name='Z', default=False)),
    ]

    rot_sym_axis : bpy.props.EnumProperty(
        name="Rot. Sym. Axis",
        description="Axis to rotate around",
        default=0,
        items= [
            ('OP1', 'X', '', 0),
            ('OP2', 'Y', '', 1),
            ('OP3', 'Z', '', 2)
        ]
    )

    symm_obj_options = [
            ('OP1', '3D Cursor', '', 0),
            ('OP2', 'Active Obj. Origin', '', 1)
    ]

    num_copies : bpy.props.IntProperty(
        name="Num. of Copies", 
        description="Number of copies", 
        default=2, 
        min=2,
        max=360,
        step=1, 
    )

    symm_obj : bpy.props.EnumProperty(  # holds the point at which the objects will be rotated around, either 3d cursor or obj's origin
        name="Rotation Origin",
        description="what to rotate around",
        default=0,
        items=symm_obj_options
    )

# ~~ OPERATORs
class RemoveMirrorMult(bpy.types.Operator):
    bl_idname = "object.remove_mirror_mult"
    bl_label = "Unmirror Selected Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):        
        selected = context.selected_objects

        for obj in selected:
            mirrorMultMods = [mod for mod in obj.modifiers if mod.name[:10] == "MirrorMult"] # creates list of all mirrormult modifiers
            if mirrorMultMods:
                obj.modifiers.remove(mirrorMultMods[-1]) # deletes the last modifier, the most recent one
        
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
            
            obj.select_set(True)

            context.view_layer.objects.active = target_obj
            target_obj.select_set(True)

            obj.modifiers[len(obj.modifiers)-1].mirror_object = target_obj  # sets the mirror object to the active object
            obj.modifiers[len(obj.modifiers)-1].use_axis = params  # sets appropriate mirror axes

            bpy.ops.object.parent_set(keep_transform=True, type='OBJECT')
            
        # the code to mirror multiple objects
        
        return {'FINISHED'}

class RotationalSymmetryOperator(bpy.types.Operator):
    bl_idname = "object.rotate_sym"
    bl_label = "Rotationally Symmetrize"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        
        collec_pref = 'RotSymCollection'
        num_items = mytool.num_copies

        target_obj = context.active_object

        obj_radius = 0
        obj_dims = 0
        obj_dims_list = [0, 0, 0]

        rot_origin_name = '' # holds the name of the object used as the origin for rotation, helps organize collections
        rot_angle = [0,0,0] # holds the angle that the empty needs to be rotated around


        if mytool.symm_obj == 'OP1':
            tool_objs = list(context.selected_objects)
            rot_origin_name = 'Cursor' # sets origin name accordingly to Cursor
            
            for obj in tool_objs:
                obj_dims = obj.dimensions

                obj_dims_list[0] += obj_dims.x
                obj_dims_list[1] += obj_dims.y
                obj_dims_list[2] += obj_dims.z
            
            for i in range(3):
                obj_dims_list[i] /= len(tool_objs) # averages out all X, Y, and Z dimensions

            obj_radius = max(obj_dims_list) * 1.1 # the largest of these dimensions is used to determine the empty's radius

        elif mytool.symm_obj == 'OP2':
            cursor_loc = scene.cursor.location # holds the past location of the cursor
            rot_origin_name = context.active_object.name # sets origin name accordingly to target_obj name
            target_obj = bpy.data.objects[rot_origin_name]
            
            obj_dims = target_obj.dimensions # used to calculate the largest dimension so that the empty object used to mirror is easily visible
            obj_dims_list = [obj_dims.x, obj_dims.y, obj_dims.z]
            obj_radius = max(obj_dims_list) * 1.1

            tool_objs = [o for o in context.selected_objects if o != target_obj]

            bpy.ops.view3d.snap_cursor_to_active() # moves 3d cursor to active object so that the empty can be placed accordingly
        
        rot_angle_num = radians((360 / num_items))
        #bpy.data.curves.new(type="FONT", name="Font Curve").body = str(num_items)

        if mytool.rot_sym_axis == 'OP1':
            rot_angle = Euler((rot_angle_num, 0, 0), 'XYZ')
        elif mytool.rot_sym_axis == 'OP2':
            rot_angle = Euler((0, rot_angle_num, 0), 'XYZ')
        elif mytool.rot_sym_axis == 'OP3':
            rot_angle = Euler((0, 0, rot_angle_num), 'XYZ')
            
        bpy.ops.object.empty_add(type='PLAIN_AXES', rotation=rot_angle, radius=obj_radius, location=scene.cursor.location)

        rotation_obj = bpy.data.objects[context.active_object.name]

        rotation_obj.name = 'RotSymObj' # renames the empty
        bpy.ops.collection.objects_remove_all() # delinks rotation_obj from all existing collections, need to rework to nest collections

        new_collec_name = collec_pref + '.' + rot_origin_name
        
        print(new_collec_name)
        
        for collec in bpy.data.collections:
            if collec.name == new_collec_name:
                new_collec_name += 'a'
        
        new_collec = bpy.data.collections.new(new_collec_name) # creates a new collection to hold all objects that will be rotationally symmetrized
        
        new_collec.objects.link(rotation_obj)

        scene.collection.children.link(new_collec)
        
        bpy.ops.object.select_all(action='DESELECT')
        
        rotation_obj.select_set(False)

        for obj in tool_objs:           
            context.view_layer.objects.active = obj
            obj.select_set(True)
            
            print(obj.name)
            
            mirrorMods = [mod for mod in obj.modifiers if mod.name[:6] == "Mirror"] # collects all mirror modifiers from the objects, since the modifier itself is based on the origin of the object and will be ruined if the rot sym is applied

            for mod in mirrorMods:
                obj.modifiers.apply_modifier(mod)

            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            bpy.ops.object.transform_apply(rotation=True, location=False)
            bpy.data.collections[-1].objects.link(obj)

            obj.modifiers.new('RotSymm', type='ARRAY')
            
            rot_sym_modifier = obj.modifiers[len(obj.modifiers)-1]
            rot_sym_modifier.use_relative_offset = False
            rot_sym_modifier.use_object_offset = True
            rot_sym_modifier.offset_object = rotation_obj
            rot_sym_modifier.count = num_items
            
            context.view_layer.objects.active = rotation_obj
            rotation_obj.select_set(True)
            
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
            
            bpy.ops.object.select_all(action='DESELECT')
            
            if rot_origin_name != 'Cursor':
                target_obj.select_set(True)
                context.view_layer.objects.active = rotation_obj
                rotation_obj.select_set(True)
                
                bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
            
            bpy.ops.object.select_all(action='DESELECT')
    
            #rot_origin_name = ''
    
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
        
        layout.label(text='Rot. Sym. Axis')
        layout.prop(mytool, "rot_sym_axis", expand=True)

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