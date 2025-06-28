import bpy
from mathutils import Vector

letters = [
    'a', 'á', 'b', 'c', 'č', 'd', 'ď', 'e', 'é', 'ě', 'f',
    'g', 'h', 'i', 'í', 'j', 'k', 'l', 'm', 'n', 'ň',
    'o', 'ó', 'p', 'q', 'r', 'ř', 's', 'š', 't', 'ť', 'u',
    'ú', 'ů', 'v', 'w', 'x', 'y', 'ý', 'z', 'ž',
    'A', 'B', 'C', 'D', 'E', 'F',
    'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
    'O', 'P', 'Q', 'R', 'S', 'T', 'U',
    'V', 'W', 'X', 'Y', 'Z',
    '.', ',', '!', '?', ':', '-', '(', ')', ' ',
]

max_row_width = 25
gap = 1
padding = 0.05
base_width = 0.015
mirror_offset_x = padding
mirror_offset_y = 0.3

block_template = bpy.data.objects.get("stamp_block")
text_template = bpy.data.objects.get("stamp_text")
if not block_template or not text_template:
    raise Exception("❌ Chybí objekt 'stamp_block' nebo 'stamp_text'")

collection = bpy.context.collection
current_x = 0
current_y = 0

for index, letter in enumerate(letters):
    block_obj = block_template.copy()
    block_obj.data = block_template.data.copy()
    block_obj.name = f"block_{index}"
    collection.objects.link(block_obj)

    text_obj = text_template.copy()
    text_obj.data = text_template.data.copy()
    text_obj.data.body = letter
    text_obj.name = f"text_{index}"
    collection.objects.link(text_obj)

    text_obj.scale.x = -abs(text_obj.scale.x)

    bpy.context.view_layer.update()

    text_width = text_obj.dimensions.x
    desired_width = max(base_width, text_width + 2 * padding)

    block_width = block_obj.dimensions.x
    if block_width > 0:
        block_obj.dimensions.x = desired_width

    bpy.context.view_layer.update()

    text_bbox = [text_obj.matrix_world @ Vector(corner) for corner in text_obj.bound_box]
    block_bbox = [block_obj.matrix_world @ Vector(corner) for corner in block_obj.bound_box]

    text_min = Vector((min(v[i] for v in text_bbox) for i in range(3)))
    block_min = Vector((min(v[i] for v in block_bbox) for i in range(3)))

    delta = (block_min.x - text_min.x + mirror_offset_x,
             block_min.y - text_min.y + mirror_offset_y,
             0)

    text_obj.location.x += delta[0]
    text_obj.location.y += delta[1]

    all_coords = []
    for obj in [block_obj, text_obj]:
        if obj.type in {'MESH', 'FONT', 'CURVE'}:
            all_coords.extend([obj.matrix_world @ Vector(corner) for corner in obj.bound_box])

    min_corner = Vector((min(c[i] for c in all_coords) for i in range(3)))
    max_corner = Vector((max(c[i] for c in all_coords) for i in range(3)))
    dims = max_corner - min_corner
    width = dims.x
    height = dims.y

    if current_x + width > max_row_width:
        current_x = 0
        current_y += height + gap

    offset_x = current_x
    offset_y = -current_y
    for obj in [block_obj, text_obj]:
        obj.location.x += offset_x
        obj.location.y += offset_y

    current_x += width + gap
    
for template_obj in [block_template, text_template]:
    if template_obj.name in bpy.data.objects:
        template_obj.select_set(False)
        if bpy.context.view_layer.objects.active == template_obj:
            bpy.context.view_layer.objects.active = None
        bpy.data.objects.remove(template_obj, do_unlink=True)
