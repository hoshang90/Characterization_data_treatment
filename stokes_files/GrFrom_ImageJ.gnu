#!/usr/bin/gnuplot -persist
set xlabel "Position ({/Symbol m}m)"
set ylabel "Intensity"
set title substr(GPVAL_PWD,26,strlen(GPVAL_PWD))
set style fill transparent solid 0.3 border
unset obj
unset lab
unset arrow
I0=48290
pr I0/exp(2)
xmin=-235
xmax=348
d=xmax-xmin
set arrow 1 from xmin,I0/exp(2) to xmax,I0/exp(2) heads
set label 1 "2w=".d."{/Symbol m}m" at xmax+30,I0/exp(2)
pl [-1000:1000] \
"profil.txt" u ($1-218)*4.4:2 w filledcurve lc rgb "dark-violet" not

