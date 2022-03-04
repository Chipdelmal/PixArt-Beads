
from os import path
from glob import glob
import auxiliary as aux

PTH="/home/chipdelmal/Documents/PixelatorBeads/AdvanceWars/BlueMoon/"
palettes = glob(path.join(PTH, '*.pal'))

palette = palettes[1]
aux.readPaletteFile(palette)

