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

def go():
    print("Texture Painter starting up.")
    cwd = os.path.dirname(bpy.data.filepath)
    # Read through the CSV
    for backer in get_backers('backers_10.csv'):
        text_to_render = backer['Name'] + ', ' + backer['Country']
        filename = cwd + '\\texture_cache\\' + backer['Number'] + '.png'
        print("Rendering", text_to_render, "to", filename)
        render_text_to_file(text_to_render, filename)
