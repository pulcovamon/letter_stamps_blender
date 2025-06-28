import bpy

bpy.ops.object.mode_set(mode='OBJECT')

for obj in bpy.data.objects:
    if obj.type == 'FONT':
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        bpy.ops.object.convert(target='MESH')
        