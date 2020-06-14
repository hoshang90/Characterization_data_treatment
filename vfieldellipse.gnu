#!/usr/bin/gnuplot
fichier="zz556x712"
fichier="zz0050x0050"
fichier="CartoTM0100x0100"
fichier="lam0p250218x0189"
L=strlen(fichier)
fichierS0=fichier."_Stokes.bin"
fichierEll=fichier."_Ellip.bin"
#fichier="test"
ech=5
Nx=fichier[L-8:L-5]*1
Ny=fichier[L-3:]*1
ray=60

set title fichier offset 0,-1
set multiplot
set size ratio 0 1,1
set encoding utf8
set angle deg
unset key
unset xtics
unset ytics

#set xrange [10:80]
#set yrange [10:80]
set view map
set linetype 4 lc rgb "white"
set linetype 6 lc rgb "black"
#--------------
set cblabel "Pixel intensity" offset 0,1
#set cbtics 20000
set lmargin at screen 0.15
set rmargin at screen 0.95
set bmargin at screen 0.15
set tmargin at screen 0.95
set colorbox front horizontal user \
 origin graph 0.01,graph -0.1 \
 size graph 0.4,graph 0.05
splot  fichierS0  binary format="%uint16%*4int8" array=(Nx,Ny) \
 flipy w image
plot  fichierEll every ech:ech binary format="%2uint8%int16%uint8"  \
array=(Nx,Ny) flipy u ($1/ray):($2/ray):3:4\
   w ellipse   units xx lc  variable
unset multiplot
