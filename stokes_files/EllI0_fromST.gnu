#!/usr/bin/gnuplot -persist
x0=word(system('MaxFWHMfromST.py'),1)
xmax=word(system('MaxFWHMfromST.py'),2)
xmin=-xmax
sample=20
set link x2 via (x+x0)/4.4 inverse (x*4.4-x0)
set xtics nomir
set x2tics nomir
set title substr(GPVAL_PWD,20,strlen(GPVAL_PWD))
set xrange [xmin:xmax]
unset arrow
unset object
unset label
unset key
unset colorbox
set palette model RGB defined ( -1.0 'red', 1.0 'green' )
sens(x)=x>=0?"red":"green"
set angle deg
set for [i=1:10] style line i linewidth 2
set style increment user
set xlabel "Camera position ({/Symbol m}m)"
set ylabel "Intensity "
set style fill transparent solid 0.03 border
rx=600./4
ry=2./8
set yrange [-1:1]
liste=system('ls ST* -tr')
set multiplot

plot for [file in liste] \
	file u ($0*4.4-x0):5 axes x1y2 \
	w filledcurve lc rgb "dark-violet" not

set style fill transparent solid 0.1 border
i=0

do  for [file in liste] {
set object ellipse center 0,-0.90+i*0.22\
 size ry*cos(0.5*file[3:]),ry*sin(0.5*file[3:]) units yy \
fc rgb  sens(sin(file[3:])) fillstyle solid .7 border lt -1

set label file[3:] at graph 0.9,first -0.90+i*0.22

plot file every sample u ($0*4.4*sample-x0):(-0.90+i*0.22):\
(ry*cos(0.5*asin($4))):(ry*abs(sin(0.5*asin($4)))):\
(0.5*atan2($3,$2)):(sin($4)>0?1:2) \
  w ellipses units yy lc  vari not 
i=i+1
}
unset multiplot
