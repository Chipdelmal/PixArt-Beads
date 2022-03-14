
from os import path
from glob import glob
import functions as aux

PTH = './palettes/'
palettes = sorted(glob(path.join(PTH, '*.plt')))
(WIDTH, HEIGHT) = (500, 20)
tRow = "<tr><td>{}</td><td><img src='./{}.png'></td><td><a href={}>{}</a></td></tr>"
###############################################################################
# Palette swatches
###############################################################################
for palette in palettes:
    pal = aux.readPaletteFile(palette)
    img = aux.genColorSwatch(pal['palette'], 500, 20)
    img.save(path.join(PTH, pal['name']+'.png'))
###############################################################################
# Text for README
###############################################################################
(head, body, tail) = ("<table><tr><th>Code</th><th>Palette</th><th>Source</th></tr>", "", "</table>")
palette = palettes[0]
for palette in palettes:
    pal = aux.readPaletteFile(palette)
    body = body+tRow.format(
        pal['name'], pal['name'], pal['source'], pal['source']
    )
print(head+body+tail)