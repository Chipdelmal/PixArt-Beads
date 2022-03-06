
from glob import glob
from sys import argv
from PIL import Image
from os import path, remove
from cv2 import imread, imwrite
import colors as col
import auxiliary as aux


if aux.isNotebook():
    (BASE_PATH, PNG_NAME, PAL_NAME, DOWNSCALE, BKGN, QNT_MTHD, DWN_MTHD) = (
        '/home/chipdelmal/Documents/PixelatorBeads/AdvanceWars/BlueMoon', 
        'rocketsPalette.png', 'NES_55.plt',
        48, ('#ff7fff', '#ffffff'), 0, Image.BILINEAR
    )
else:
    (BASE_PATH, PNG_NAME, DOWNSCALE) = (argv[1], argv[2], int(argv[3]))
###############################################################################
# Load Image
###############################################################################
pth = path.join(BASE_PATH, PNG_NAME)
img = Image.open(pth).convert('RGB')
###############################################################################
# Replace Background Color
###############################################################################
if BKGN is not None:
    img = aux.replaceBackground(img, BKGN[0], replacementColor=BKGN[1])
###############################################################################
# Quantize
#   0: median cut, 1: maximum coverage, 2: fast octree
###############################################################################
palDict = aux.readPaletteFile(path.join(BASE_PATH, PAL_NAME))
cpal = aux.paletteReshape(palDict['palette'])
imgQnt = aux.quantizeImage(
    img, colorsNumber=cpal[0], colorPalette=cpal[1], method=QNT_MTHD
)
###############################################################################
# Downscale
#   Image.NEAREST, Image.BILINEAR, Image.BICUBIC, Image.LANCZOS, Image.NEAREST
###############################################################################
dsize = aux.downscaleSize(img, DOWNSCALE)
imgQnt.resize(dsize, resample=DWN_MTHD)