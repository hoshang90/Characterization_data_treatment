#!/usr/bin/gnuplot -persist
load "/usr/local/share/stokes/BasePoincare.gnu"
set view 62,67
fichier="stokes"
#attention , il y a un espace à la fin!!!
lignes="1050 1100 "
teta=40
tilt=11
psi=-118

system('ST2stokes.py '.lignes.fichier)
angles=system('ST2teta.py '.fichier)
set vrange [0:psi]
set title substr(GPVAL_PWD,26,strlen(GPVAL_PWD))
rmp=1.5
set arrow 7 from rmp*ux(teta,tilt),rmp*uy(teta,tilt),rmp*uz(teta,tilt) to\
 -rmp*ux(teta,tilt),-rmp*uy(teta,tilt),-rmp*uz(teta,tilt) \
heads lc rgb "red" lw 2

set label 1  at  rmp*ux(teta,tilt),rmp*uy(teta,tilt),rmp*uz(teta,tilt) "MP" front

splot \
"/usr/local/share/stokes/boule50.dat" u 1:2:3:($3) w pm3d not,\
"/usr/local/share/stokes/meridiens.dat" w l lt -1 dt "." not,\
cos(u),0,sin(u) w l lt -1 not,\
S1(cos(u),sin(u),psi),S2(cos(u),sin(u),psi),S3(cos(u),sin(u),psi)\
 w l lw 1 lt -1\
 t"S3=".sprintf("%.2f (%.1f)",sin(2*teta),teta)."\nPsi=".sprintf("%.1f",psi)\
."\nTilt=".sprintf("%.1f",tilt),\
for [xs in angles]\
S1(cos(xs),sin(xs),v),S2(cos(xs),sin(xs),v),S3(cos(xs),sin(xs),v)\
w l lc rgb "orange-red" not,\
fichier u 1:(0):3 w p  pt 7 lc  rgb "orange-red" ps 2 lw 1 not,\
"" u 1:(0):3:0 w labels not,\
"" u 5:6:7 w p pt 6 lc rgb "orange-red" ps 2 lw 1  not,\
"" u 5:6:7:0 w labels  not,\
"" u (S1($1,$3,psi)):(S2($1,$3,psi)):(S3($1,$3,psi)) w p pt 1 ps 2 lt -1 not

