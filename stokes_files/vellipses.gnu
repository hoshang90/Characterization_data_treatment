#!/usr/bin/gnuplot -persist
#default 640x480
# 1600x900 par ecran ou 3200x900
set term qt size 550,400 position 2000,440
set angle rad
unset label
unset arrow
unset object
#:cal SetSyn("gnuplot")
#unset key
 #set angle deg
set st d lp
set xlabel "E_x"
set ylabel "E_y"
unset xlabel
unset ylabel
unset xtics
unset ytics
unset key
set border 0
set size square
f(x)=abs(tan(x))<1? abs(tan(x)):1./abs(tan(x))
#set yrange [-15:15]
set style line 1 lt rgb "red" pt 7
set style line 2 lt rgb "red" pt 6
set style line 3 lt rgb "royalblue" pt 9
set style line 4 lt rgb "royalblue" pt 8
rgbfudge(x) = x*51*32768 + (11-x)*51*128 + int(abs(5.5-x)*510/9.)
sIn(x)=tan(x)<=0?rgbfudge(1):rgbfudge(10)
sOut(x)=tan(x)<=0?rgbfudge(1):rgbfudge(10)
set colorbox
set label 1 "Input polarisation ellipse" \
at graph 0.2, graph 0.2 rotate by 90
set label 2 "Output polarisation ellipse" \
at graph 0.8, graph 0.2 rotate by 90
r0=3
r1=4
rtod=180/pi
unset label

pl  "ellipse"\
 u (r0*cos(2*$1)):(r0*sin(2*$1)):(abs(cos($1))):(abs(sin($1))) \
   w ell units xx lw 2  lc rgb "red" fs solid 0.3\
 t "Input Ellipse",\
"" u (r1*cos(2*$1)):(r1*sin(2*$1)):(abs(cos($2))):(abs(sin($2))):($3*rtod) \
   w ell units xx lw 2 \
lc rgb "green" fs solid 0.3 t "Output Ellipse",\
"" u (0):(0):(r1*cos(2*$1)):(r1*sin(2*$1)) w vect nohead lt 0 not
#,\
#"" u (-0.3):(f($1)):(+0.3):(0) i 1 with vectors filled  front not,\
#EOF
#"" u (f($1)):(0.05):(2):(2*abs(tan($2))):(90+$3) \
#i 1   w ell units xx t "Ellip TM"
