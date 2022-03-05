
import numpy as np
from os import path
from glob import glob
import auxiliary as aux
from PIL import Image, ImageColor

imgName = "aaPalette"
PTH = "/home/chipdelmal/Documents/PixelatorBeads/AdvanceWars/BlueMoon/"
filename = path.join(PTH, imgName+'.png')
palettes = glob(path.join(PTH, '*.pal'))

###############################################################################
# Palette Load
###############################################################################
palette = palettes[1]
aux.readPaletteFile(palette)

###############################################################################
# Color Replace
###############################################################################
bkgColor = '#ff7fff'
orig_color = ImageColor.getcolor(bkgColor, "RGB")
replacement_color = (255, 255, 255)

img = Image.open(filename).convert('RGB')
aux.replaceBackground(img, bkgColor, replacementColor='#ffffff')

