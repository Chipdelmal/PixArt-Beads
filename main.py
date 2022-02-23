
from os import path, remove
from PIL import Image
from cv2 import imread, imwrite
import colors as col
import auxiliary as aux


(fld, nme) = ('/home/chipdelmal/Documents/PixelatorBeads', 'sniper.png')
(downscale, upscale) = (60, 20)
(colorsNumber, method) = (25, 1)
###############################################################################
# Color Palettes
###############################################################################
PALS = (
    col.COLD_WOOD, col.NOSTALGIA, col.GB, col.ENDESAGA, col.NES,
    col.SLSO, col.MASTEROS, col.SGB_A, col.SGB_B, col.SGB_C, 
    col.SGB_D, col.SUPER_ST, col.MF_SXT, col.ARTKAL_48, col.PEAR_36, 
    col.PIXLTEN, col.ZANT, col.SWEETIE_16, None
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
    # Load Image
    ###########################################################################
    pth = path.join(fld, nme)
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
    upscaleSize = (upscale*downscale[0], upscale*downscale[1])
    img = img.resize(upscaleSize, Image.NEAREST)
    ###########################################################################
    # Save Scaled Image
    ###########################################################################
    pth = '{}-{}-{}'.format(paletteName, str(downscale[0]), nme)
    pthUG = path.join(fld, aux.pthUG+pth)
    img.save(pthUG)
    ###########################################################################
    # Add grid onto the image
    ###########################################################################
    img = imread(pthUG)
    img = aux.gridOverlay(img, upscale, gridColor=(0, 0, 0))
    # remove(pthUG)
    imwrite(path.join(fld, aux.pthGD+pth), img)
    