import os
from PIL import Image, ImageDraw

def create_icon(size):
    # Create a simple blue shield icon
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Shield coordinates (roughly)
    pad = size * 0.1
    w = size - 2*pad
    h = size - 2*pad
    points = [
        (pad, pad),
        (size-pad, pad),
        (size-pad, size-pad*3),
        (size/2, size-pad),
        (pad, size-pad*3)
    ]
    draw.polygon(points, fill=(37, 99, 235)) # #2563EB Blue
    
    return img

os.makedirs('d:/phishscope/extension/icons', exist_ok=True)
create_icon(16).save('d:/phishscope/extension/icons/16.png')
create_icon(48).save('d:/phishscope/extension/icons/48.png')
create_icon(128).save('d:/phishscope/extension/icons/128.png')
print("Icons generated.")
