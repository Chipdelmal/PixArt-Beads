
import cv2
import numpy as np
from os.path import exists
from glob import glob
from sys import argv
from PIL import Image, ImageColor
from os import path, remove
from cv2 import imread, imwrite, cvtColor
import matplotlib.pyplot as plt
import colors as col
import auxiliary as aux


if aux.isNotebook():
    (BASE_PATH, PNG_NAME, PAL_NAME) = (
        '/home/chipdelmal/Documents/PixelatorBeads/AdvanceWars/BlueMoon', 
        'rocketsPalette.png', 'GB_5.plt'
    )
    (DOWNSCALE, UPSCALE, QNT_MTHD, DWN_MTHD) = (48, 10, 0, Image.BILINEAR)
else:
    (BASE_PATH, PNG_NAME, DOWNSCALE) = (argv[1], argv[2], int(argv[3]))

(outRadius, inRadius, bgColor, imgAlpha) = (.975 , .2, '#eeeeee', .9)
###############################################################################
# Folders and Filenames
###############################################################################
fID = PNG_NAME.split('.')[0]
outFolder = path.join(BASE_PATH, fID)
aux.makeFolder(outFolder)
(pthQNT, pthDWN, pthUPS, pthGRD, pthSWT, pthBDS, pthFNL) = [
    path.join(outFolder, i+f'_{fID}.png') for i in aux.FIDS
]
###############################################################################
# Load Image
###############################################################################
pth = path.join(BASE_PATH, PNG_NAME)
img = Image.open(pth).convert('RGB')
###############################################################################
# Replace Background Color
###############################################################################
fileMapper = path.join(BASE_PATH, 'CMapper.map')
if exists(fileMapper):
    cMapper = aux.readCMapperFile(fileMapper)
    img = aux.mapColors(img, cMapper)
###############################################################################
# Quantize
#   0: median cut, 1: maximum coverage, 2: fast octree
###############################################################################
palDict = aux.readPaletteFile(path.join(BASE_PATH, PAL_NAME))
cpal = aux.paletteReshape(palDict['palette'])
imgQnt = aux.quantizeImage(
    img, colorsNumber=cpal[0], colorPalette=cpal[1], method=QNT_MTHD
)
# imgQnt.save(pthQNT)
###############################################################################
# Downscale
#   Image.NEAREST, Image.BILINEAR, Image.BICUBIC, Image.LANCZOS, Image.NEAREST
###############################################################################
dsize = aux.downscaleSize(imgQnt, DOWNSCALE)
imgDwn = imgQnt.resize(dsize, resample=DWN_MTHD)
imgDwn.save(pthDWN)
###############################################################################
# Upscale
###############################################################################
upscaleSize = [UPSCALE*i for i in dsize]
imgUps = imgDwn.resize(upscaleSize, Image.NEAREST)
imgUps.save(pthUPS)
###############################################################################
# Gridded
###############################################################################
imgTmp = imread(pthUPS)
imgGrd = aux.gridOverlay(imgTmp, UPSCALE, gridColor=(0, 0, 0))
imwrite(pthGRD, imgGrd)
###############################################################################
# Beads Plot
###############################################################################
imgTmp = imread(pthDWN)
(fig, ax) = aux.genBeadsPlot(
    imgTmp, bgColor=bgColor,
    outRadius=outRadius, inRadius=inRadius, imgAlpha=imgAlpha
)
plt.savefig(
    pthBDS, 
    bbox_inches='tight', pad_inches=0, dpi=200,
    facecolor=[i/255 for i in ImageColor.getcolor(bgColor, "RGB")]
)
plt.close('all')
###############################################################################
# Swatch
###############################################################################
(imgBDS, imgTmp) = (
    Image.open(pthBDS).convert('RGB'),
    Image.open(pthDWN).convert('RGB')
)
swatch = aux.getImagePalette(imgTmp)
imgSwt = aux.genColorCounts(swatch, 500, imgBDS.size[1])
plt.savefig(
    pthSWT, 
    bbox_inches='tight', pad_inches=0,
    facecolor=[i/255 for i in ImageColor.getcolor(bgColor, "RGB")]
)
plt.close('all')
###############################################################################
# Final Figure
###############################################################################
(imgBDS, imgSWT) = (
    Image.open(pthBDS).convert('RGB'),
    Image.open(pthSWT).convert('RGB')
)
ccat = aux.hConcat(imgBDS, imgSWT)
ccat.save(pthFNL)

