#!/usr/bin/gnuplot -persist
x0=0
set for [i=1:10] style line i linewidth 2
set style increment user
set ylabel "S_3"
set xlabel "Camera position ({/Symbol m}m)"
set y2label "Intensity "
set style fill transparent solid 0.2 border

pl []\
"ST0" u ($0*4.4-x0):5 axes x1y2 \
w filledcurve lc rgb "dark-violet" not ,\
"" u ($0*4.4-x0):($5>500?$4:1/0)  lt 2  t " TE S_3",\
"" u ($0*4.4-x0):($5>500?$2/$1:1/0)  lt 2 dt ".."  t "TE S_2/S_1"
#"ST90" u ($0*4.4-x0):5 axes x1y2 \
#w filledcurve lc rgb "dark-violet" not ,\
#"" u ($0*4.4-x0):($5>500?$4:1/0)  lt 3  t " CG S_3",\
#"" u ($0*4.4-x0):($5>500?$2/$1:1/0)  lt 3 dt ".."  t "CG S_2/S_1",\
#"ST180" u ($0*4.4-x0):5 axes x1y2 \
#w filledcurve lc rgb "dark-violet" not ,\
#"" u ($0*4.4-x0):($5>500?$4:1/0)  lt 4  t " TM S_3",\
#"" u ($0*4.4-x0):($5>500?$2/$1:1/0)  lt 4 dt ".."  t "TM S_2/S_1"
