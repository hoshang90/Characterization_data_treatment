#!/usr/bin/gnuplot -persist
# installer le paquet gnuplot5-doc
 set term gif animate transparent opt delay 20 size 480,480 background rgb 'black'
set outp "anim.gif"
load "/usr/local/share/stokes/BasePoincare.gnu"
unset xlabel
unset ylabel
unset zlabel
set view 62,67
fichier="stokes"
#attention , il y a un espace à la fin!!!
lignes="600 640 "
teta=9.5
tilt=1.8
psi=-79.6

system('ST2stokes.py '.lignes.fichier)
angles=system('ST2teta.py '.fichier)

# Defines for gnuplot.rot script
limit_iterations=72
xrot=60
xrot_delta = 0
zrot=136
zrot_delta = 355
xview(xrot)=xrot
zview(zrot)=zrot
set view xview(xrot), zview(zrot)
set size square
unset key
unset title
unset key
unset xtics
unset ytics
unset ztics
set border 0



set vrange [0:psi]
rmp=1.5
set arrow 7 from rmp*ux(teta,tilt),rmp*uy(teta,tilt),rmp*uz(teta,tilt) to\
 -rmp*ux(teta,tilt),-rmp*uy(teta,tilt),-rmp*uz(teta,tilt) \
heads lc rgb "red" lw 2


splot \
"/usr/local/share/stokes/boule50.dat" u 1:2:3:($3) w pm3d not,\
"/usr/local/share/stokes/meridiens.dat" w l lt -1 dt "." not,\
cos(u),0,sin(u) w l lt -1 not,\
S1(cos(u),sin(u),psi),S2(cos(u),sin(u),psi),S3(cos(u),sin(u),psi)\
 w l lw 1 lt -1 not,\
for [xs in angles]\
S1(cos(xs),sin(xs),v),S2(cos(xs),sin(xs),v),S3(cos(xs),sin(xs),v)\
w l lc rgb "orange-red" not,\
fichier u 1:(0):3 w p  pt 7 lc  rgb "orange-red" ps 2 lw 1 not,\
"" u 1:(0):3:0 w labels not,\
"" u 5:6:7 w p pt 6 lc rgb "orange-red" ps 2 lw 1  not,\
"" u 5:6:7:0 w labels  not,\
"" u (S1($1,$3,psi)):(S2($1,$3,psi)):(S3($1,$3,psi)) w p pt 1 ps 2 lt -1 not

iteration_count=0
xrot =(xrot+xrot_delta)%360
zrot =(zrot+zrot_delta)%360

load "/usr/share/doc/gnuplot5-doc/examples/gnuplot.rot"
set outp 
set term qt

