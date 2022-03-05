# https://matplotlib.org/stable/tutorials/colors/colors.html

import numpy as np
from os import path
from glob import glob
import auxiliary as aux
from PIL import Image, ImageColor
from matplotlib import rcParams
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
rcParams['font.family'] = ''


imgName = "aaPalette"
PTH = "/home/chipdelmal/Documents/PixelatorBeads/AdvanceWars/BlueMoon/"
filename = path.join(PTH, imgName+'.png')
palettes = sorted(glob(path.join(PTH, '*.plt')))

###############################################################################
# Palette Load
###############################################################################
palette = palettes[1]
pal = aux.readPaletteFile(palette)
aux.genColorSwatch(pal['palette'], 500, 20)
###############################################################################
# Color Replace
###############################################################################
img = Image.open(filename).convert('RGB')
imgP = aux.replaceBackground(img, '#ff7fff', replacementColor='#ffffff')
###############################################################################
# Color Palette
###############################################################################
imgPalette = aux.getImagePalette(imgP)
###############################################################################
# Color Palette
###############################################################################
(wpx, hpx) = (250, 2300)
fontdict = {'family':'monospace', 'weight':'bold', 'size':22}
aux.genColorCounts(imgPalette, wpx, hpx)


# Setting up figure size
fig = plt.gcf()
DPI = fig.get_dpi()
ax = fig.add_axes([0, 0, 1, 1])
fig.set_size_inches(wpx/float(DPI), hpx/float(DPI))
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
    ax.add_patch(mpatch.Rectangle((0+col_shift, y_pos), wr, hr, color=rgb, ec='k'))
    ax.text(
        wr*1.1+col_shift, y_pos+hr/2, f'{color} ({count:04})', 
        color='k', va='center', ha='left', fontdict=fontdict
    )
# Clean up the axes
ax.set_xlim(0, .5*n_groups)
ax.set_ylim((n_rows), -1)
ax.axis('off')


fig.savefig("test.png", dpi=DPI)

    


