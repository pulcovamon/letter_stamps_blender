import bpy
from mathutils import Vector

def get_bbox_xy(obj):
    coords = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    xs = [v.x for v in coords]
    ys = [v.y for v in coords]
    return min(xs), max(xs), min(ys), max(ys)

def bbox_overlap_xy(obj1, obj2):
    min_x1, max_x1, min_y1, max_y1 = get_bbox_xy(obj1)
    min_x2, max_x2, min_y2, max_y2 = get_bbox_xy(obj2)
    return not (max_x1 < min_x2 or max_x2 < min_x1 or max_y1 < min_y2 or max_y2 < min_y1)

bpy.ops.object.mode_set(mode='OBJECT')
mesh_names = [obj.name for obj in bpy.data.objects if obj.type == 'MESH']

for base_name in mesh_names:
    base = bpy.data.objects.get(base_name)
    if base is None:
        continue

    for other_name in mesh_names:
        if other_name == base_name:
            continue

        other = bpy.data.objects.get(other_name)
        if other is None:
            continue

        if not bbox_overlap_xy(base, other):
            continue

        bpy.ops.object.select_all(action='DESELECT')
        base.select_set(True)
        other.select_set(True)
        bpy.context.view_layer.objects.active = base

        bpy.ops.object.join()
        break
