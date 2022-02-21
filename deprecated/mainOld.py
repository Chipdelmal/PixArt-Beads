import cv2
import numpy as np
from PIL import Image

def pixelateImage(img, gridSize, gridOverlay=True, gridOverlayColor=(0, 0, 0)):
    # Run through the image and apply a mean filter function
    for r in range(0, img.shape[0], gridSize):
        for c in range(0, img.shape[1], gridSize):
            block = img[r:r+gridSize, c:c+gridSize, :]
            shp = block.shape
            blurred = cv2.blur(block, (shp[0]*2, shp[1]*2))
            img[r:r+gridSize, c:c+gridSize, :] = blurred
            # Could export here if the blocks were needed
    # Overlay the grid if requested
    if gridOverlay is True:
        # Add Gridlines
        height, width, channels = img.shape
        for x in range(0, width - 1, gridSize):
            cv2.line(img, (x, 0), (x, height), gridOverlayColor, 1, 1)

        for x in range(0, height - 1, gridSize):
            cv2.line(img, (0, x), (width, x), gridOverlayColor, 1, 1)

    return img


img = cv2.imread('./img/fighter.png', cv2.IMREAD_UNCHANGED)

scaleMult = 5

scale_percent = scaleMult * 100 # percent of original size
width = int(img.shape[1]*scale_percent/100)
height = int(img.shape[0]*scale_percent/100)
dim = (width, height)

resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

img = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
im_pil = Image.fromarray(img)
imQnt = im_pil.quantize(5, method=0)
imQnt.save("./img/A_fighter.png")

img = cv2.imread('./img/A_fighter.png')
imgO = pixelateImage(img, scaleMult, gridOverlay=True)
cv2.imwrite('./img/B_fighter.png', imgO)


