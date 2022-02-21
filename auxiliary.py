###############################################################################
#   Functions Definitions
###############################################################################

import cv2
import numpy as np
from PIL import Image, ImageColor

(pthUG, pthGD) = ('A_', 'B_')

def paletteReshape(colorPalette):
    # Hex to entries
    rgbTuples = [ImageColor.getrgb(i) for i in colorPalette]
    pal = [item for sublist in rgbTuples for item in sublist]
    entries = int(len(pal)/3)
    # Palette swatch
    palette = pal + [0,]*(256-entries)*3
    resnp = np.arange(entries, dtype=np.uint8).reshape(entries, 1)
    resim = Image.fromarray(resnp, mode='P')
    resim.putpalette(palette)
    # Return
    return (len(pal), resim)


def quantizeImage(img, colorsNumber=255, colorPalette=None, method=0, dither=False):
    if colorPalette is None:
        img = img.quantize(colorsNumber, method=method, dither=dither)
    else:
        img = img.quantize(
            palette=colorPalette, method=method, dither=dither
        )
    return img


def gridOverlay(img, gridSize, gridColor=(0,0,0)):
    img = np.asarray(img)
    (height, width, channels) = img.shape
    for x in range(0, width-1, gridSize):
        cv2.line(img, (x, 0), (x, height), gridColor, 1, 1)
    for x in range(0, height-1, gridSize):
        cv2.line(img, (0, x), (width, x), gridColor, 1, 1)
    return img