
import os
import cv2
from os import path
from sys import argv
from glob import glob
from cv2 import imread, cvtColor
import matplotlib.pyplot as plt
import auxiliary as aux

if aux.isNotebook():
    PNG_NAME = 'lynnSword'
else:
    PNG_NAME = argv[1]
os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")
fldr = '/home/chipdelmal/Documents/PixelatorBeads'
(outRadius, inRadius) = (.975 , .2)
(bgColor, imgAlpha) = ((.9, .9, .9), .9)
###############################################################################
# Needed to run the dev phase
###############################################################################
nme = '{}.png'.format(PNG_NAME)
pthOut = path.join(fldr, PNG_NAME)
inImages = glob(path.join(pthOut, '{}*-{}'.format(aux.PPND[0], nme)))
###############################################################################
# Iterate processed images
###############################################################################
imPth = inImages[0]
for imPth in inImages:
    (prep, palName, name) = path.basename(imPth).split('-')
    (nmeUnscaled, nmeBeads) = (
        '{}{}-{}'.format(aux.PPND[0], palName, nme[:-4]),
        '{}{}-{}'.format(aux.PPND[3], palName, nme[:-4])
    )
    ###########################################################################
    # Process images
    ###########################################################################
    img = imread(path.join(pthOut, nmeUnscaled+'.png'))
    img = cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
    (fig, ax) = plt.subplots(1, 1, figsize=(15, 15))
    aux.plotBeads(
        fig, ax, img, 
        innerRadius=inRadius, outerRadius=outRadius,
        imgAlpha=imgAlpha, bgColor=bgColor
    )
    plt.savefig(
        path.join(pthOut, nmeBeads), 
        bbox_inches='tight', pad_inches=0, facecolor=bgColor, dpi=200
    )
    plt.close('all')
