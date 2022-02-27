#!/bin/bash

PTH="/home/chipdelmal/Documents/PixelatorBeads"
FNAME=$1
SCALE=$2

echo "* Downscaling and quantizing..."
python imgProcess.py $1 $2
echo "* Generating bead plots..."
python beadPlot.py $1