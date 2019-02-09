"""Renders text from a CSV file to textures
and applies them to multiple objectsself.

Use Snippets...
## To load path on start
import os, sys; sys.path.append(os.path.dirname(bpy.data.filepath)); import texture_painter

## To reload after a code changes
import importlib; importlib.reload(texture_painter); texture_painter.go()
"""

import codecs, csv, os, bpy
from PIL import Image, ImageFont, ImageDraw

def get_backers(csv_filename):
    with codecs.open (csv_filename, 'r', 'utf-8-sig') as stream:
        iterable = csv.reader(stream)
        header = next(iterable)
        for row in iterable:
            backer = dict(zip(header, row))
            yield backer

#image size and font-size hard-coded in method
def render_text_to_file(text_to_render, to_filename):
    image = Image.new('RGB', (512,64))
    draw = ImageDraw.Draw(image)
    fnt = ImageFont.truetype('snake.ttf', 50)
    draw.text((0,0), text_to_render, font=fnt, fill=(255,255,255))
    image.save(to_filename)

def throw_invalid_selection():
    if len(bpy.context.selected_objects) == 0:
        raise Exception("Please select exactly one prototype object")
    if len(bpy.context.selected_objects) > 1:
        raise Exception("Please select exactly one prototype object")

def create_plaque(prototype, offset):
    prototype.select = True
    bpy.ops.object.duplicate_move(TRANSFORM_OT_translate={"value":offset})
    new_plaque = bpy.context.selected_objects[0]
    new_plaque.select = False
    return new_plaque

def blender_render_select():
    bpy.context.scene.render.engine = "BLENDER_RENDER"

def get_offset(num, columns, spacing):
    """Return offset from prototype position.
    Positional arguments:
    num -- the number of the object, starting from 0
    columns -- how many columns before wrapping
    spacing -- a tuple of (x,y), spacing between objects
    """
    x_offset = (num % columns) * spacing[0] # x-spacing
    y_offset = (num // columns) * spacing[1] # y-spacing
    return (x_offset, y_offset)

def swap_text(object, backer, index):
    cwd = os.path.dirname(bpy.data.filepath)
    text_to_render = backer['Name'] + ', ' + backer['Country']
    filename = cwd + '\\texture_cache\\' + str(index) + '.png'
    render_text_to_file(text_to_render, filename)
    print("Swapping tecture to:", backer) # TODO actual swap

def go():
    print("Texture Painter starting up.")
    blender_render_select()
    print("Blender Render Selected")
    throw_invalid_selection()
    print("Prototype object found.")
    prototype = bpy.context.selected_objects[0]
    for num, backer in enumerate(get_backers('backers_10.csv')):
        if num == 0:
            plaque = prototype
        else:
            x, y = get_offset(num, 3, (2,-1,0))
            plaque = create_plaque(prototype, (x,y,0))
        swap_text(plaque, backer, num)
