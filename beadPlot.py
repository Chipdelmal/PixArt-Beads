
import cv2
from os import path
from cv2 import imread, cvtColor
import matplotlib.pyplot as plt
import auxiliary as aux
import colors as col

PNG_NAME = 'lynn'
fldr = '/home/chipdelmal/Documents/PixelatorBeads'
colDict = col.ENDESAGA
(outRadius, inRadius) = (.975 , .2)
(bgColor, alpha) = ((1, 1, 1), .9)
###############################################################################
# Neded to run the dev phase
###############################################################################
(paletteName, colorPalette) = (colDict['name'], colDict['palette'])
nme = '{}.png'.format(PNG_NAME)
pthOut = path.join(fldr, PNG_NAME)
(nmeUnscaled, nmeBeads) = (
    '{}{}-{}'.format(aux.PPND[0], paletteName, nme),
    '{}{}-{}'.format(aux.PPND[3], paletteName, nme)
)
###############################################################################
# Dev
###############################################################################
img = imread(path.join(pthOut, nmeUnscaled))
img = cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
(fig, ax) = plt.subplots(1, 1, figsize=(15, 15))
aux.plotBeads(
    fig, ax, img, 
    innerRadius=inRadius, outerRadius=outRadius,
    imgAlpha=alpha, bgColor=bgColor
)
plt.savefig(
    path.join(pthOut, nmeBeads), 
    bbox_inches='tight', pad_inches=0, facecolor=bgColor, dpi=200
)
plt.close('all')
