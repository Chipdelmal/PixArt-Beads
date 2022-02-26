
from turtle import bgcolor
import cv2
from os import path
from cv2 import imread, cvtColor
import matplotlib.pyplot as plt
import auxiliary as aux
import colors as col

(PNG_NAME, downscale) = ('mechYellow', 48)
fldr = '/home/chipdelmal/Documents/PixelatorBeads'
colDict = col.GB
(diameter, scaler, center) = (1, .95 , .2)
bgColor = (1, 1, 1)
alpha = .9
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
(width, height, _) = img.shape

radius = diameter/2
(fig, ax) = plt.subplots(1, 1, figsize=(15, 15), sharey=False)
for h in range(int(height)):
    y = diameter*h
    for w in range(int(width)):
        x = diameter * w
        coord = (width-x, height-y)
        crl = plt.Circle(
            coord, radius*scaler, 
            color=tuple([i/255 for i in img[x][y]]), alpha=alpha
        )
        crlV = plt.Circle(coord, radius*center, color=bgColor)
        ax.add_patch(crl)
        ax.add_patch(crlV)
ax.set_xlim(radius, width+radius)
ax.set_ylim(radius, height+radius)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_facecolor(bgColor)
ax.set_aspect(1)
ax.axis('off')
plt.savefig(
    path.join(pthOut, nmeBeads), 
    bbox_inches='tight', pad_inches=0, facecolor=bgColor, dpi=200
)