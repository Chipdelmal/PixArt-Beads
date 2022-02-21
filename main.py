
from os import path
from PIL import Image
from cv2 import imread, imwrite
import colors as col
import auxiliary as aux


# Folder (fld): Working directory for input and output images
# Name (nme): Original image's name
# Downscale: (w, h) tuple of the number of pixels of our beads pattern
# Upscale: Multiplier scaler to upscale our pixelated image for easy reading
# Colors Number (colorsNumber): Number of colors to be used in the quantization
#   process (overridden if the color palette is provided)
# Color Palette (colorPalette): List of HEX values to be used in the 
#   quantization of the image. Set color palette to "None" to use the 
#   colorsNumber parameter instead.
# Method (int):
#   0 = median cut
#   1 = maximum coverage
#   2 = fast octree

# (fld, nme) = ('./img', 'APC.png')
(fld, nme) = ('/home/chipdelmal/Documents/PixelatorBeads', 'mech.png')
(downscale, upscale) = ((32, 32), 20)
(colorsNumber, method) = (3, 0)
colorPalette = col.SLSO

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