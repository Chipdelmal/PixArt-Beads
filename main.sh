#!/bin/bash

NME='sami.png'
PTH="/home/chipdelmal/Documents/PixelatorBeads/AdvanceWars/Portraits"
DWN="0"
UPS="10"

###############################################################################
# Get color palettes in folder
###############################################################################
FILES=($(find $PTH -name '*.plt'))
# for f in "${FILES[@]}"; do echo "$f"; done
###############################################################################
# Process files
###############################################################################
for val in ${FILES[@]}; do
    PAL=$(basename ${val})
    echo "* Processing ${PAL}"
    python main.py $PTH $NME $PAL $DWN $UPS
done
