# PixArt Beads

This repo contains some python scripts that should be useful in transforming images into pixel-beads images and handcrafts!

<img src="./media/sami.png" height="200px"><img src="./media/B-SGB_M1A-sami.png" height="200px" ><img src="./media/C-SGB_M1A-sami.png" height="200px"><img src="./media/D-SGB_M1A-sami.png" height="200px">


Some of the main features are:

* **Color quantization:** with the option to use number of colors, provided or user-defined color palettes.
* **Image downscale:** take an image and downsize it to a desired number of pixels.
* **Color mapping:** manually change colors to do things like remove the background.
* **Color counts:** count the number of beads of each color that are needed for our handcraft.

## Instructions

**IMPORTANT NOTE:** For a step-by-step use of the scripts, please have a look at the provided [demo](./demo) after installing the dependencies.

To use the scripts first install the required dependencies either through the REQUIREMENTS files (`txt`/`yml`), or manually:

```bash
pip install numpy
pip install Pillow
pip install matplotlib
pip install opencv-python
```

Give the bash script executable permissions:

```bash
chmod +x main.sh
```

And then run it as follows:

```bash
./main.sh $PTH $IMG $DWN $UPS $DBG
```

`PTH`: Folder in which our image(s) are stored along with the palettes and color mapper.
`IMG`: Image name for the file to be processed.
`DWN`: Width in pixels for our output image (leave as `0` if no downscaling is desired).
`UPS`: Upscaler multiplier for the plots (`10`, the suggested value, will multiply the dimensions of the downscaled images by ten when exporting the output).
`DBG`: Debug mode (leave as `0` if no intermediary output is desired, and as `1` to have each intermediate plot exported).

This will take the `IMG` in the set `PTH` along with all the `*.plt` files stored in the directory and the `CMapper.map`, and generate a nested output folder (in the same directory) with the bead plots. Alternatively, we can use the `batch.sh` file to process all the images stored in the same directory:

```bash
./batch.sh $PTH $DWN $UPS $DBG
```

Finally, the script can also be called from python with:

```bash
python main.py $PTH $IMG $PAL $DWN $UPS $DBG
```

where an additional parameter `PAL` is needed for the color palette filename (if set to a number instead of a `.plt` file, it will instead quantize to the provided number of colors.

## Available Palettes

Some nice [color palettes](./palettes/README.md) are included in the scripts, but if you have the hex colors of your beads, please follow [this link](./palettes/README.md) for information on how to use them in your handcraft! A subset of the included palettes is shown but follow the [link for the full list](./palettes/README.md):

<table>
    <tr><th>Code</th><th>Palette</th><th>Source</th></tr>
    <!--Table Begins-->
    <tr><td>CoolWood_8</td><td><img src='./palettes/CoolWood_8.png'></td><td><a href=https://lospec.com/palette-list/coldwood8>https://lospec.com/palette-list/coldwood8</a></td></tr>
    <tr><td>Gray2Bit_4</td><td><img src='./palettes/Gray2Bit_4.png'></td><td><a href=https://lospec.com/palette-list/2-bit-grayscale>https://lospec.com/palette-list/2-bit-grayscale</a></td></tr>
    <tr><td>IslandJoy_16</td><td><img src='./palettes/IslandJoy_16.png'></td><td><a href=https://lospec.com/palette-list/island-joy-16>https://lospec.com/palette-list/island-joy-16</a></td></tr>
    <tr><td>MF_16</td><td><img src='./palettes/MF_16.png'></td><td><a href=https://lospec.com/palette-list/mf-16>https://lospec.com/palette-list/mf-16</a></td></tr>
    <tr><td>Mist_GB</td><td><img src='./palettes/Mist_GB.png'></td><td><a href=https://lospec.com/palette-list/mist-gb>https://lospec.com/palette-list/mist-gb</a></td></tr>
    <tr><td>NES</td><td><img src='./palettes/NES.png'></td><td><a href=https://lospec.com/palette-list/nintendo-entertainment-system>https://lospec.com/palette-list/nintendo-entertainment-system</a></td></tr>
    <tr><td>Nostalgia_36</td><td><img src='./palettes/Nostalgia_36.png'></td><td><a href=https://lospec.com/palette-list/nostalgia36>https://lospec.com/palette-list/nostalgia36</a></td></tr>
    <tr><td>Super_16</td><td><img src='./palettes/Super_16.png'></td><td><a href=https://lospec.com/palette-list/super16>https://lospec.com/palette-list/super16</a></td></tr>
    <tr><td>Sweetie_16</td><td><img src='./palettes/Sweetie_16.png'></td><td><a href=https://lospec.com/palette-list/sweetie-16>https://lospec.com/palette-list/sweetie-16</a></td></tr>
</table> 

##  Author

<img src="./media/pusheen.jpg" height="100px" align="middle"><br>

[Héctor M. Sánchez C.](https://chipdelmal.github.io/)
