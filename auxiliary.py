###############################################################################
#   Functions Definitions
###############################################################################

import re
import os
import cv2
import numpy as np
from PIL import Image, ImageColor
from cv2 import imread, cvtColor
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch

PPND = ('A-', 'B-', 'C-', 'D-')
FIDS = ('QNT', 'DWN', 'UPS', 'GRD', 'SWT', 'BDS', 'FNL')
MTHDS = (0, Image.BILINEAR)
RADII = (0.2, 0.975)
(BEAD_ALPHA, BEAD_BKG) = (0.9, '#fefefe')

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


def genBeadsPlot(
        imgCV, diameter=1, outRadius=0.975, inRadius=0.2, 
        imgAlpha=.9, bgColor='#ffffff'
    ):
    bkgCol = [i/255 for i in ImageColor.getcolor(bgColor, "RGB")]
    imgCV = cvtColor(imgCV, cv2.COLOR_BGR2RGB)
    imgCV = cv2.rotate(imgCV, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
    (fig, ax) = plt.subplots(1, 1, figsize=(15, 15))
    (fig, ax) = plotBeads(
        fig, ax, imgCV, diameter=diameter,
        innerRadius=inRadius, outerRadius=outRadius,
        imgAlpha=imgAlpha, bgColor=bkgCol
    )
    return (fig, ax)


def readPaletteFile(filePath, hexPtrn=r'^#(?:[0-9a-fA-F]{3}){1,2}$'):
    with open(filePath) as f:
        lines = f.read().splitlines() 
    (name, source, colors) = (lines[0], lines[1], lines[2:])
    colors = [c for c in colors if re.search(hexPtrn, c)]
    colorPalette = {'name': name, 'source': source, 'palette': colors}
    return colorPalette


def readCMapperFile(filePath):
    with open(filePath) as f:
        lines = f.read().splitlines()
    cMapper = [[i.strip() for i in l.split(',')] for l in lines]
    cMapper = [i for i in cMapper if len(i) > 1]
    return cMapper


def replaceBackground(img, bkgColor, replacementColor='#ffffff'):
    # Convert HEX to RGB
    orig_color = ImageColor.getcolor(bkgColor, "RGB")
    replacement_color = ImageColor.getcolor(replacementColor, "RGB")
    # Replace color
    data = np.array(img)
    data[(data==orig_color).all(axis=-1)] = replacement_color
    img2 = Image.fromarray(data, mode='RGB')
    return img2


def mapColors(img, cMapper=(('#ff7fff', '#ffffff'))):
    for i in cMapper:
        img = replaceBackground(img, i[0], replacementColor=i[1])
    return img


def rgbToHex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def getImagePalette(img):
    palette = sorted(img.getcolors(), reverse=True)
    hexPalette = [(rgbToHex(*i[1]), i[0]) for i in palette]
    return hexPalette



def genColorSwatch(palette, width, height):
    colors = [ImageColor.getcolor(i, "RGB") for i in palette]
    clstNumber = len(colors)
    pltAppend = np.zeros((height, width, 3))
    (wBlk, hBlk) = (round(width/clstNumber), round(height))
    for row in range(hBlk):
        colorIter = -1
        for col in range(width):
            if (col%wBlk == 0) and (colorIter < clstNumber-1):
                colorIter = colorIter + 1
            pltAppend[row][col] = colors[colorIter]
    return Image.fromarray(pltAppend.astype('uint8'), 'RGB')


def getLuma(r, g, b):
    luma = 0.299*r + 0.587*g + 0.114*b
    return luma


def genColorCounts(
        imgPalette, width, height, imgSize, upscale,
        fontdict = {'family':'monospace', 'weight':'normal', 'size':37.5},
        xlim = (0, 1.25)
    ):
    pal = imgPalette
    # Create canvas
    fig = plt.gcf()
    DPI = fig.get_dpi()
    ax = fig.add_axes([0, 0, 1, 1])
    fig.set_size_inches(width/float(DPI), height/float(DPI))
    # Setting up groups
    n_groups = 1
    n_rows = len(pal)//n_groups+1
    # Generate swatch with count
    for j in range(len(pal)):
        (wr, hr) = (.25, 1)
        (color, count) = pal[j]
        rgb = [i/255 for i in ImageColor.getcolor(color, "RGB")]
        # Color rows
        col_shift = (j//n_rows)*3
        y_pos = (j%(n_rows))*hr
        # Print rectangle and text
        hshift = .05
        ax.add_patch(mpatch.Rectangle(
            (hshift+col_shift, y_pos), wr, hr, color=rgb, ec='k', lw=4
        ))
        colorText = color.upper()
        ax.text(
            hshift+wr*1.1+col_shift, y_pos+hr/2, 
            f' {colorText} ({count:05}) ', 
            color='k', va='center', ha='left', fontdict=fontdict
        )
    # Add pixel size and total count
    pxSize = [int(i/upscale) for i in imgSize]
    y_pos = ((0)%(n_rows))*hr
    ax.text(
        hshift, y_pos-hr/2, 
        f'Size: {pxSize[0]}x{pxSize[1]}', 
        color='k', va='center', ha='left', fontdict=fontdict
    )
    y_pos = ((j+1)%(n_rows))*hr
    ax.text(
        hshift, y_pos+hr/2, 
        f'Total: {pxSize[0]*pxSize[1]}', 
        color='k', va='center', ha='left', fontdict=fontdict
    )
    # Clean up the axes
    ax.set_xlim(xlim[0], xlim[1]*n_groups)
    ax.set_ylim((n_rows), -1)
    ax.axis('off')
    # Return figure
    return (fig, ax)


def downscaleSize(img, downscale):
    if downscale == 0:
        downscale = img.size
    else:
        if type(downscale) is not tuple:
            (wo, ho) = img.size
            downscale = (downscale, int((ho/wo)*downscale))
    return downscale


def makeFolder(path):
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except OSError:
            raise OSError(
                    "Can't create destination directory (%s)!" % (path)
                )


def hConcat(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def vConcat(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


def isInt(element):
    try:
        int(element)
        return True
    except ValueError:
        return False
