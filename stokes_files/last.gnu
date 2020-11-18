#!/usr/bin/gnuplot --persist
#default 640x480
# 1600x900 par ecran ou 3200x900
set term qt size 550,400 position 1600,2

set polar
set angle deg
set xtics axis nomirror
set ytics axis nomirror
unset rtics
set clip
unset border
set zeroaxis
set size square
pl "Last" t "Output",\
"" u 1:3 t "Fit",\
"" u 1:4 t "Input"
