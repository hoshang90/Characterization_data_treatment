#!/usr/bin/gnuplot -persist
x0=word(system('MaxFWHMfromST.py'),1)
xmin=word(system('MaxFWHMfromST.py'),2)
set xrange [-xmin:xmin]
set yrange [-1:1]
set for [i=1:10] style line i linewidth 2
set style increment user
set ylabel "S_3"
set xlabel "Camera position ({/Symbol m}m)"
set y2label "Intensity "
set style fill transparent solid 0.2 border
liste=system('ls ST*')
i=0
unset arrow
unset object
unset label
set angle deg
set multiplot


plot for [file in liste] \
	file u ($0*4.4-x0):5 axes x1y2 \
	w filledcurve lc rgb "dark-violet" not
plot for [file in liste] \
	file u ($0*4.4-x0):($5>500?$4:1/0)   t file[3:]

plot for [file in liste] \
	file u ($0*4.4-x0):(abs($0*4.4-x0)<50?sin(file[3:]):1/0)   dt ".._"  not
#plot for [file in liste]  file u ($0*4.4-x0):($5>500?$3/$2:1/0)   dt ".."  not
unset multiplot
