# Color Palette Files

The color palette files are nothing else than text files saved with a **.plt** extension. This *ad hoc* format follows this structure:

```bash
PALETTE_NAME
PALETTE_SOURCE
HEX_1
HEX_2
...
HEX_N
```

Where the two first rows will always be interpreted as palette name and palette source. The name is mandatory as it is used to generate the filenames of the output files. The source is optional but do **leave the line blank in case no "source" value is provided** (otherwise the palette reader will skip the color entered in this position).

**Important Note**: Please note that the included color palettes are not mine. They were obtained from https://lospec.com/palette-list/, so please visit the palette sources and support the authors' work if possible!