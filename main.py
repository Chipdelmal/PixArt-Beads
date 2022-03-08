
import os
from sys import argv
from os.path import exists
from os import path, remove
from cv2 import imread, imwrite
import matplotlib.pyplot as plt
from PIL import Image, ImageColor
import auxiliary as aux

if aux.isNotebook():
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
(QNT_MTHD, DWN_MTHD) = (aux.MTHDS[0], aux.MTHDS[1])
###############################################################################
# Folders and Filenames
###############################################################################
(fID, palID) = (PNG_NAME.split('.')[0], PAL_NAME.split('.')[0])
outFolder = path.join(BASE_PATH, fID)
aux.makeFolder(outFolder)
(pthQNT, pthDWN, pthUPS, pthGRD, pthSWT, pthBDS, pthFNL) = [
    path.join(outFolder, i+f'-{palID}-{fID}.png') for i in aux.FIDS
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
if aux.isInt(PAL_NAME):
    imgQnt = aux.quantizeImage(img, int(PAL_NAME), method=QNT_MTHD)
else:
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
    imgTmp, bgColor=aux.BEAD_BKG,
    inRadius=aux.RADII[0], outRadius=aux.RADII[1], imgAlpha=aux.BEAD_ALPHA
)
plt.savefig(
    pthBDS, bbox_inches='tight', pad_inches=0, dpi=100,
    facecolor=[i/255 for i in ImageColor.getcolor(aux.BEAD_BKG, "RGB")]
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
imgSwt = aux.genColorCounts(swatch, 500, imgBDS.size[1], imgBDS.size, UPSCALE)
plt.savefig(
    pthSWT, bbox_inches='tight', pad_inches=0,
    facecolor=[i/255 for i in ImageColor.getcolor(aux.BEAD_BKG, "RGB")]
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
###############################################################################
# Delete files
###############################################################################
banList = (pthDWN, pthUPS, pthGRD, pthSWT, pthBDS, pthFNL)
if not DEBUG:
    for tFile in banList[:-1]:
        remove(tFile)