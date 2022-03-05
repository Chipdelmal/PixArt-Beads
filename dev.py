
import numpy as np
from os import path
from glob import glob
import auxiliary as aux
from PIL import Image, ImageColor

imgName = "aaPalette"
PTH = "/home/chipdelmal/Documents/GitHub/PixelatorBeads/palettes/"
filename = path.join(PTH, imgName+'.png')
palettes = sorted(glob(path.join(PTH, '*.plt')))

###############################################################################
# Palette Load
###############################################################################
palette = palettes[0]
for palette in palettes:
    pal = aux.readPaletteFile(palette)
    img = aux.genColorSwatch(pal, 500, 20)
    img.save(path.join(PTH, pal['name']+'.png'))

for palette in palettes:
    pal = aux.readPaletteFile(palette)
    print("<tr><td>{}</td><td><img src='./palettes/{}.png'></td><td><a href={}>{}</a></td></tr>".format(pal['name'], pal['name'], pal['source'], pal['source']))
###############################################################################
# Color Replace
###############################################################################
img = Image.open(filename).convert('RGB')
imgP = aux.replaceBackground(img, '#ff7fff', replacementColor='#ffffff')
###############################################################################
# Color Palette
###############################################################################
aux.getImagePalette(imgP)
