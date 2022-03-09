
import os
from sys import argv
from time import sleep
from os.path import exists
from os import path, remove
from cv2 import imread, imwrite
import matplotlib.pyplot as plt
from PIL import Image, ImageColor
import functions as fun

if fun.isNotebook():
    (BASE_PATH, PNG_NAME, PAL_NAME) = (
        '/home/chipdelmal/Documents/PixelatorBeads/AdvanceWars/BlueMoon', 
        'cruiserPalette.png', 'Sweetie_16.plt'
    )
    (DOWNSCALE, UPSCALE) = (48, 10)
    DEBUG = True
else:
    os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")
    (BASE_PATH, PNG_NAME, PAL_NAME) = (argv[1], argv[2], argv[3])
    (DOWNSCALE, UPSCALE) = (int(argv[4]), int(argv[5]))
    DEBUG = int(argv[6])
# Internal constants ----------------------------------------------------------
(QNT_MTHD, DWN_MTHD) = (fun.MTHDS[0], fun.MTHDS[1])
###############################################################################
# Folders and Filenames
###############################################################################
(fID, palID) = (PNG_NAME.split('.')[0], PAL_NAME.split('.')[0])
outFolder = path.join(BASE_PATH, fID)
fun.makeFolder(outFolder)
(pthQNT, pthDWN, pthUPS, pthGRD, pthSWT, pthBDS, pthFNL) = [
    path.join(outFolder, i+f'-{palID}-{fID}.png') for i in fun.FIDS
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
    cMapper = fun.readCMapperFile(fileMapper)
    img = fun.mapColors(img, cMapper)
###############################################################################
# Quantize
#   0: median cut, 1: maximum coverage, 2: fast octree
###############################################################################
if fun.isInt(PAL_NAME):
    imgQnt = fun.quantizeImage(img, int(PAL_NAME), method=QNT_MTHD)
else:
    palDict = fun.readPaletteFile(path.join(BASE_PATH, PAL_NAME))
    cpal = fun.paletteReshape(palDict['palette'])
    imgQnt = fun.quantizeImage(
        img, colorsNumber=cpal[0], colorPalette=cpal[1], method=QNT_MTHD
    )
# imgQnt.save(pthQNT)
###############################################################################
# Downscale
#   Image.NEAREST, Image.BILINEAR, Image.BICUBIC, Image.LANCZOS, Image.NEAREST
###############################################################################
dsize = fun.downscaleSize(imgQnt, DOWNSCALE)
imgDwn = imgQnt.resize(dsize, resample=DWN_MTHD)
imgDwn.save(pthDWN)
sleep(fun.SLEEP)
###############################################################################
# Upscale
###############################################################################
upscaleSize = [UPSCALE*i for i in dsize]
imgUps = imgDwn.resize(upscaleSize, Image.NEAREST)
imgUps.save(pthUPS)
sleep(fun.SLEEP)
###############################################################################
# Gridded
###############################################################################
imgTmp = imread(pthUPS)
imgGrd = fun.gridOverlay(imgTmp, UPSCALE, gridColor=(0, 0, 0))
imwrite(pthGRD, imgGrd)
sleep(fun.SLEEP)
###############################################################################
# Beads Plot
###############################################################################
imgTmp = imread(pthDWN)
(fig, ax) = fun.genBeadsPlot(
    imgTmp, bgColor=fun.BEAD_BKG,
    inRadius=fun.RADII[0], outRadius=fun.RADII[1], imgAlpha=fun.BEAD_ALPHA
)
plt.savefig(
    pthBDS, bbox_inches='tight', pad_inches=0, dpi=100,
    facecolor=[i/255 for i in ImageColor.getcolor(fun.BEAD_BKG, "RGB")]
)
plt.close('all')
sleep(fun.SLEEP)
###############################################################################
# Swatch
###############################################################################
(imgBDS, imgTmp, imgDwn) = (
    Image.open(pthBDS).convert('RGB'),
    Image.open(pthDWN).convert('RGB'),
    Image.open(pthDWN).convert('RGB')
)
swatch = fun.getImagePalette(imgTmp)
imgSwt = fun.genColorCounts(swatch, 500, imgBDS.size[1], imgDwn.size)
plt.savefig(
    pthSWT, bbox_inches='tight', pad_inches=0,
    facecolor=[i/255 for i in ImageColor.getcolor(fun.BEAD_BKG, "RGB")]
)
plt.close('all')
sleep(fun.SLEEP)
###############################################################################
# Final Figure
###############################################################################
(imgBDS, imgSWT) = (
    Image.open(pthBDS).convert('RGB'),
    Image.open(pthSWT).convert('RGB')
)
ccat = fun.hConcat(imgBDS, imgSWT)
ccat.save(pthFNL)
sleep(fun.SLEEP)
###############################################################################
# Delete files
###############################################################################
banList = (pthDWN, pthUPS, pthGRD, pthSWT, pthBDS, pthFNL)
if not DEBUG:
    for tFile in banList[:-1]:
        remove(tFile)