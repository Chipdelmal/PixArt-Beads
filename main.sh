#!/bin/bash

PTH="/home/chipdelmal/Documents/PixelatorBeads/AdvanceWars/OrangeStar"
DWN="0"
UPS="10"
DBG="0"

BLU='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'
###############################################################################
# Get PNGs and Palettes in folder
###############################################################################
PNGS=($(find $PTH -name '*.png'))
FILES=($(find $PTH -name '*.plt'))
# for f in "${FILES[@]}"; do echo "$f"; done
###############################################################################
# Process files
###############################################################################
for nme in ${PNGS[@]}; do
    FNM=$(basename ${nme})
    for val in ${FILES[@]}; do
        PAL=$(basename ${val})
        printf "\r* Processing ${BLU}${FNM} ${RED}[${PAL}]\033[K${NC}"
        # printf "* Processing ${BLU}${FNM} ${RED}[${PAL}]\n"
        python main.py $PTH $FNM $PAL $DWN $UPS $DBG
    done
done
printf "\r\n"