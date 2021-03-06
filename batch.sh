#!/bin/bash

###############################################################################
# PixArt Beads
# -----------------------------------------------------------------------------
#   PTH: Path to where the images are stored, along with palettes and cmapper
#   DWN: Downscale width in px (if set to 0, it will maintain the original)
#   UPS: Upscale multiplier (10x is recommended for most images)
#   DBG: Debug mode (set to 1 for all the intermediate images to be kept)
###############################################################################
PTH=$1 # "/home/chipdelmal/Documents/PixelatorBeads/AdvanceWars/Portraits"
DWN=$2 # "0"
UPS=$3 # "10"
DBG=$4 # "1"
###############################################################################
# Get Palettes in folder
###############################################################################
PNGS=($(find $PTH -name '*.png'))
###############################################################################
# Process files
###############################################################################
for nme in ${PNGS[@]}; do
    FNM=$(basename ${nme})
    source main.sh $PTH $FNM $DWN $UPS $DBG
done
printf "\r\n"