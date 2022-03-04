# PixelatorBeads


<img src="./media/sami.png" height="225px" align="middle"><img src="./media/B-SGB_M1A-sami.png" height="225px" align="middle"><img src="./media/C-SGB_M1A-sami.png" height="225px" align="middle"><img src="./media/D-SGB_M1A-sami.png" height="225px" align="middle">

## Instructions

To use the script first install the required dependencies:

```bash
pip install numpy
pip install Pillow
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



##  Author

<img src="./media/pusheen.jpg" height="100px" align="middle"><br>

[Héctor M. Sánchez C.](https://chipdelmal.github.io/)
