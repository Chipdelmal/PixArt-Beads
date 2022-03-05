
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
img = Image.open(filename).convert('RGB')
imgP = aux.replaceBackground(img, '#ff7fff', replacementColor='#ffffff')
###############################################################################
# Color Palette
###############################################################################
aux.getImagePalette(imgP)
