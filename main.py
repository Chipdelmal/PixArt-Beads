
from sys import argv
from os import path, remove
from PIL import Image
from cv2 import imread, imwrite
import colors as col
import auxiliary as aux


if aux.isNotebook():
    (PNG_NAME, downscale) = ('sami', 48)
else:
    (PNG_NAME, downscale) = (argv[1], int(argv[2]))
fldr = '/home/chipdelmal/Documents/PixelatorBeads'
(colorsNumber, method, upscale) = (25, 1, 10)
saveStages = (True, True, True)
###############################################################################
# Directories and Names
###############################################################################
nme = '{}.png'.format(PNG_NAME)
pthOut = path.join(fldr, PNG_NAME)
aux.makeFolder(pthOut)
###############################################################################
# Color Palettes
###############################################################################
PALS = (
    col.COLD_WOOD, col.NOSTALGIA, col.GB, col.ENDESAGA, col.NES,
    col.SLSO, col.MASTEROS, col.SGB_A, col.SGB_B, col.SGB_C, 
    col.SGB_D, col.SUPER_ST, col.MF_SXT, col.ARTKAL_48, col.PEAR_36, 
    col.PIXLTEN, col.ZANT, col.SWEETIE_16, col.BLK_NEO, col.FAMICUBE,
    col.ONE_BIT, col.BLESSING, col.ISLANDJOY_16, col.AMMO_8, col.GRAY_2BIT,
    col.RESURRECT_32, col.LUX2K, col.MIST_GB, col.COMFORT_44, col.TWILIGHT_5,
    None
)
###############################################################################
# Iterate Through Palettes
###############################################################################
for colDict in PALS:
    if colDict is not None:
        (paletteName, colorPalette) = (colDict['name'], colDict['palette'])
    else:
        (paletteName, colorPalette) = (str(colorsNumber), None)
    ###########################################################################
    # Setup Output Names
    ###########################################################################
    (nmeUnscaled, nmeUngridded, nmeGridded) = (
        '{}{}-{}'.format(aux.PPND[0], paletteName, nme),
        '{}{}-{}'.format(aux.PPND[1], paletteName, nme),
        '{}{}-{}'.format(aux.PPND[2], paletteName, nme)
    )
    ###########################################################################
    # Load Image
    ###########################################################################
    pth = path.join(fldr, nme)
    img = Image.open(pth).convert('RGB')
    ###########################################################################
    # Check Scale
    ###########################################################################
    if type(downscale) is not tuple:
        (wo, ho) = img.size
        downscale = (downscale, int((ho/wo)*downscale))
    ###########################################################################
    # Quantize
    ###########################################################################
    if colorPalette is not None:
        cpal = aux.paletteReshape(colorPalette)
        img = aux.quantizeImage(
            img, colorsNumber=cpal[0], colorPalette=cpal[1], method=method
        )
    else:
        img = aux.quantizeImage(img, colorsNumber, method=method)
    ###########################################################################
    # Downscale and Upscale
    ###########################################################################
    img = img.resize(downscale, resample=Image.BILINEAR)
    if saveStages[0]:
        img.save(path.join(pthOut, nmeUnscaled))
    upscaleSize = (upscale*downscale[0], upscale*downscale[1])
    img = img.resize(upscaleSize, Image.NEAREST)
    ###########################################################################
    # Save Scaled Image
    ###########################################################################
    img.save(path.join(pthOut, nmeUngridded))
    ###########################################################################
    # Add grid onto the image
    ###########################################################################
    img = imread(path.join(pthOut, nmeUngridded))
    img = aux.gridOverlay(img, upscale, gridColor=(0, 0, 0))
    if not saveStages[1]:
        remove(pthUG)
    if saveStages[2]:
        imwrite(path.join(pthOut, nmeGridded), img)
    