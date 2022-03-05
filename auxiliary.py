###############################################################################
#   Functions Definitions
###############################################################################

import re
import os
import cv2
import numpy as np
from PIL import Image, ImageColor
import matplotlib.pyplot as plt

PPND = ('A-', 'B-', 'C-', 'D-')


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


def makeFolder(path):
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except OSError:
            raise OSError(
                    "Can't create destination directory (%s)!" % (path)
                )

def isNotebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True
        elif shell == 'TerminalInteractiveShell':
            return False
        else:
            return False
    except NameError:
        return False


def plotBeads(
        fig, ax, img, diameter=1,
        innerRadius=.2, outerRadius=.975,
        imgAlpha=.9, bgColor=(1, 1, 1)
    ):
    radius = diameter/2
    (width, height, _) = img.shape
    # Iterate through pixels 
    for h in range(int(height)):
        y = (diameter*h)
        for w in range(int(width)):
            x = (diameter*w)
            coord = (width-x, height-y)
            # Plot solid disk
            crl = plt.Circle(
                coord, radius*outerRadius, 
                color=tuple([i/255 for i in img[x][y]]), alpha=imgAlpha
            )
            ax.add_patch(crl)
            # Plot empty center
            crlV = plt.Circle(coord, radius*innerRadius, color=bgColor)
            ax.add_patch(crlV)
    # Clean the frame
    ax.set_xlim(radius, width+radius)
    ax.set_ylim(radius, height+radius)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_facecolor(bgColor)
    ax.set_aspect(1)
    ax.axis('off')
    # Return figure
    return (fig, ax)


def readPaletteFile(filePath, hexPtrn=r'^#(?:[0-9a-fA-F]{3}){1,2}$'):
    with open(filePath) as f:
        lines = f.read().splitlines() 
    (name, source, colors) = (lines[0], lines[1], lines[2:])
    colors = [c for c in colors if re.search(hexPtrn, c)]
    colorPalette = {'name': name, 'source': source, 'palette': colors}
    return colorPalette


def replaceBackground(img, bkgColor, replacementColor='#ffffff'):
    # Convert HEX to RGB
    orig_color = ImageColor.getcolor(bkgColor, "RGB")
    replacement_color = ImageColor.getcolor(replacementColor, "RGB")
    # Replace color
    data = np.array(img)
    data[(data==orig_color).all(axis=-1)] = replacement_color
    img2 = Image.fromarray(data, mode='RGB')
    return img2