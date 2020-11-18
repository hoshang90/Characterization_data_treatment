#!/usr/bin/gnuplot
reset
# their red, green, and blue components 24 bits
    rgb(r,g,b) = 65536 * int(r) + 256 * int(g) + int(b)

fichier=ARG1
#fichier="test"
ech=int(ARG2)
dx=0.9*ech/255.
b2a=180./2**15
set title fichier offset 0,-1
set multiplot
set size ratio 0 1,1
set encoding utf8
set angle rad
unset key
unset xtics
unset ytics
Noctets=system('stat -c%s '.fichier)
Npts=int(sqrt(Noctets/8))

#set xrange [10:80]
#set yrange [10:80]
set view map
set linetype 8 lc rgb "white"
set linetype 9 lc rgb "black"
#--------------
set cblabel "Pixel intensity" offset 0,1
set cbtics 20000
set lmargin at screen 0.15
set rmargin at screen 0.95
set bmargin at screen 0.15
set tmargin at screen 0.95
set colorbox front horizontal user \
 origin graph 0.01,graph -0.1 \
 size graph 0.4,graph 0.05
splot  fichier  binary format="%ushort%*3char%*short%*uchar"\
 array=(Npts,Npts) flipx w image
plot  fichier every ech:ech binary \
format="%*ushort%*char%uchar%uchar%short%uchar"  \
array=(Npts,Npts)  u (dx*$1):(dx*$2):($3*b2a):($4+8)\
   w ellipse  lc  variable
unset multiplot
