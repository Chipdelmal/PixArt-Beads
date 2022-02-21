

import cv2
import numpy as np
from os import path
from PIL import Image, ImageColor
from sklearn.cluster import MiniBatchKMeans

(fld, nme) = ('./img', 'mech.png')

pth = path.join(fld, nme)
(downscale, upscale) = ((50, 50), 10)
COL_PLT = ['#F4F4F4', '#00852B','#040404', '#58AB41', '#969696']
CLRS_NUM = 4

CLR = COL_PLT

# Color palettes
if CLRS_NUM is None:
    rgbTuples = [ImageColor.getrgb(i) for i in CLR]
    pal = [item for sublist in rgbTuples for item in sublist]
    entries = int(len(pal)/3)

# Open Paddington
img = Image.open(pth).convert('RGB')
# background = Image.new('RGBA', img.size, (0, 0, 255))
# img = Image.alpha_composite(background, img)

# Quantize result
if CLRS_NUM is None:
    palette = pal + [0,]*(256-entries)*3
    resnp = np.arange(entries, dtype=np.uint8).reshape(entries, 1)
    resim = Image.fromarray(resnp, mode='P')
    resim.putpalette(palette)
    img = img.quantize(len(COL_PLT), method=0, palette=resim, dither=False)
else:
    img = img.quantize(CLRS_NUM, method=0, dither=False)

# Resize smoothly down to 16x16 pixels
img = img.resize(downscale,resample=Image.BILINEAR)

# Scale back up using NEAREST to original size
newSize = (upscale*downscale[0], upscale*downscale[1])
img = img.resize(newSize, Image.NEAREST)
img

# Save PIL image
img.save(path.join(fld, 'A_'+nme))

(gridSize, gridOverlayColor) = (upscale, (0, 0, 0))
img = cv2.imread(path.join(fld, 'A_'+nme))
(height, width, channels) = img.shape
for x in range(0, width-1, gridSize):
    cv2.line(img, (x, 0), (x, height), gridOverlayColor, 1, 1)
for x in range(0, height-1, gridSize):
    cv2.line(img, (0, x), (width, x), gridOverlayColor, 1, 1)

# Save CV2 image
cv2.imwrite(path.join(fld, 'B_'+nme), img)
