
from os import path
from PIL import Image
from cv2 import imread, imwrite
import colors as col
import auxiliary as aux


(fld, nme) = ('./img', 'mech.png')
(downscale, upscale) = ((50, 50), 10)
(colorsNumber, colorPalette) = (10, col.GB) # col.NOSTALGIA)
method = 0

###############################################################################
# Load Image
###############################################################################
pth = path.join(fld, nme)
img = Image.open(pth).convert('RGB')
###############################################################################
# Quantize
###############################################################################
if colorPalette is not None:
    cpal = aux.paletteReshape(colorPalette)
    img = aux.quantizeImage(
        img, colorsNumber=cpal[0], colorPalette=cpal[1], method=method
    )
else:
    img = aux.quantizeImage(img, colorsNumber, method=method)
###############################################################################
# Downscale and Upscale
###############################################################################
img = img.resize(downscale, resample=Image.BILINEAR)
upscaleSize = (upscale*downscale[0], upscale*downscale[1])
img = img.resize(upscaleSize, Image.NEAREST)
###############################################################################
# Save Scaled Image
###############################################################################
pthUG = path.join(fld, aux.pthUG+nme)
img.save(pthUG)
###############################################################################
# Add grid onto the image
###############################################################################
img = imread(pthUG)
img = aux.gridOverlay(img, upscale)
imwrite(path.join(fld, aux.pthGD+nme), img)