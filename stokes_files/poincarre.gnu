#!/usr/bin/gnuplot -persist
# set terminal pngcairo  transparent font "arial,10" fontscale 1.0 size 600, 400 
# set output 'world2.1.png'
#default 640x480
# 1600x900 par ecran ou 3200x900
set term qt size 590,440 position 2600,420
unset polar
unset border
set dummy u, v
set angles degrees
set parametric
#set view 60, 136, 1.22, 1.26
set samples 64, 64
set isosamples 21, 21
#set mapping spherical
set style data lines
set noxtics
set noytics
set noztics
set urange [ -180.0000 : 180.0000 ] noreverse nowriteback
set vrange [ 0.00000 : 360.000 ] noreverse nowriteback
#set cblabel "GeV" 
#set cbrange [ 0.00000 : 8.00000 ] noreverse nowriteback
#set colorbox user
#set colorbox vertical origin screen 0.9, 0.2, 0 size screen 0.02, 0.75, 0 front bdefault
#u = 0.0
#set pm3d depthorder  
unset colorbox
set style fill  transparent solid 0.05 noborder
set palette rgb 7,5,15;
set palette gray
set pm3d at s
#unset surf
#set pm3d depthorder 
set palette rgb 3,3,3
set hidden3d  front
#unset hidden3d
#unset pm3d
unset contour
unset key
ray=0.95
splot ray*cos(u)*cos(v),ray*cos(u)*sin(v),ray*sin(u) notitle with lines lt -1 dt ".",\
cos(v),sin(v),0 w l lt 7,\
"stokes" u 1:(0):3 w lp  pt 7 lc  rgb "red" ps 2 lw 2,\
"" u 5:6:7 w lp pt 7 lc rgb "green" ps 2 lw 2,\
""  u 1:(0):3:($5-$1):6:($7-$3) w vect lt 0
