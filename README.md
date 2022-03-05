# PixArt Beads

This repo contains some python scripts that should be useful in transforming images into pixel-beads images and handcrafts!

<img src="./media/sami.png" height="200px"><img src="./media/B-SGB_M1A-sami.png" height="200px" ><img src="./media/C-SGB_M1A-sami.png" height="200px"><img src="./media/D-SGB_M1A-sami.png" height="200px">

Some of the features are:

* Color quantization: with the option to use number of colors, provided or user-defined color palettes.
* Image downscale: 
* Image upscale:
* Color replace:
* Color mapping: 
* Color palette:
* Color counts:

## Instructions

To use the scripts first install the required dependencies either through the REQUIREMENTS files (txt/yml), or manually:

```bash
pip install numpy
pip install Pillow
pip install matplotlib
pip install opencv-python
```

And, ideally, give the bash script executable permissions:

```bash
chmod +x beadify.sh
```


Then have a look at the following parameters:

* Folder (fld): Working directory for input and output images
* Name (nme): Original image's name
* Downscale: (w, h) tuple of the number of pixels of our beads pattern
* Upscale: Multiplier scaler to upscale our pixelated image for easy reading
* Colors Number (colorsNumber): Number of colors to be used in the quantization process (overridden if the color palette is provided)
* Color Palette (colorPalette): List of HEX values to be used in the quantization of the image. Set color palette to "None" to use the colorsNumber parameter instead.
* Method (int): [0: median cut, 1: maximum coverage, 2: fast octree]

## Available Palettes

Some nice [color palettes](./palettes/README.md) are included in the scripts, but if you have the hex colors of your beads, please follow [this link](./palettes/README.md) for information on how to use them in your handcraft!

##  Author

<img src="./media/pusheen.jpg" height="100px" align="middle"><br>

[Héctor M. Sánchez C.](https://chipdelmal.github.io/)
