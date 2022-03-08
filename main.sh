#!/bin/bash

###############################################################################
# PixArt Beads
# -----------------------------------------------------------------------------
#   PTH: Path to where the image is stored along with palettes and cmapper
#   IMG: Image name with extension (PNG files only)
#   DWN: Downscale width in px (if set to 0, it will maintain the original)
#   UPS: Upscale multiplier (10x is recommended for most images)
#   DBG: Debug mode (set to 1 for all the intermediate images to be kept)
###############################################################################
PTH=$1
IMG=$2
DWN=$3
UPS=$4
DBG=$5
# PTH="/home/chipdelmal/Documents/PixelatorBeads/AdvanceWars/OrangeStar"
# IMG="tcopterPalette.png"
# DWN="0"
# UPS="10"
# DBG="0"
###############################################################################
# Terminal colors
###############################################################################
BLU='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'
###############################################################################
# Get Palettes in folder
###############################################################################
PALS=($(find $PTH -name '*.plt'))
###############################################################################
# Process files
###############################################################################
for palPath in ${PALS[@]}; do
    PAL=$(basename ${palPath})
    printf "\r* Processing ${BLU}${IMG} ${RED}[${PAL}]\033[K${NC}"
    python main.py $PTH $IMG $PAL $DWN $UPS $DBG
done
printf "\r\r\n"