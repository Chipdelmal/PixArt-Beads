# https://matplotlib.org/stable/tutorials/colors/colors.html

import numpy as np
from os import path
from glob import glob
import auxiliary as aux
from PIL import Image, ImageColor
from matplotlib import rcParams
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
rcParams['font.family'] = ''


imgName = "rocketsPalette"
PTH = "/home/chipdelmal/Documents/PixelatorBeads/AdvanceWars/BlueMoon/"
filename = path.join(PTH, imgName+'.png')
palettes = sorted(glob(path.join(PTH, '*.plt')))

###############################################################################
# Palette Load
###############################################################################
palette = palettes[1]
pal = aux.readPaletteFile(palette)
swatch = aux.genColorSwatch(pal['palette'], 500, 20)
swatch
###############################################################################
# Color Replace
###############################################################################
img = Image.open(filename).convert('RGB')
imgP = aux.replaceBackground(img, '#ff7fff', replacementColor='#ffffff')
imgP
###############################################################################
# Color Palette
###############################################################################
imgPalette = aux.getImagePalette(imgP)
imgPalette
###############################################################################
# Color Palette
###############################################################################
(wpx, hpx) = (250, 2300)
aux.genColorCounts(imgPalette, wpx, hpx)
# fig.savefig("test.png")
###############################################################################
# Color Mapping
###############################################################################
cMapper = aux.readCMapperFile(path.join(PTH, 'CMapper.map'))
aux.mapColors(img, cMapper)