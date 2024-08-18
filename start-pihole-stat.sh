#!/bin/bash
clear
echo "Starting stats dashboard for 2in13g epaper"

cd $(dirname $0)/python

python stats.py
