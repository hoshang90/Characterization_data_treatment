set style fill  transparent solid 0.4 noborder
set style rectangle back fc  bgnd fillstyle   solid 1.00 border lt -1
set style circle radius graph 0.02, first 0, 0 
set style ellipse size graph 0.05, 0.03, first 0 angle 0 units xy
set dummy u, v
set angles degrees
unset grid
set raxis
set key noopaque
set label 1 "S1" at 1.5, 0, 0.1 left norotate back nopoint
set label 2 "S2" at 0, 1.55, 0 left norotate back nopoint
set label 3 "S3" at 0, 0, 1.55 left norotate back nopoint
unset arrow
set arrow 1 from -1.6, 0, 0 to 1.9, 0, 0 head back nofilled lt black linewidth 1.000 dashtype solid
set arrow 2 from 0, -1.6, 0 to 0, 1.9, 0 head back nofilled lt black linewidth 1.000 dashtype solid
set arrow 3 from 0, 0, -1.6 to 0, 0, 1.9 head back nofilled lt black linewidth 1.000 dashtype solid
set arrow 4 from 1.2, -0.2, 0 to 1.2, 0.2, 0 heads back nofilled lt black linewidth 2.000 dashtype solid
set arrow 5 from -1.2, 0, -0.2 to -1.2, 0, 0.2 heads back nofilled lt black linewidth 2.000 dashtype solid
set arrow 6 from 0, 1.26, 0.14 to 0, 1.54, -0.14 heads back nofilled lt black linewidth 2.000 dashtype solid
set arrow 7 from 0, -1.26, 0.14 to 0, -1.54, -0.14 heads back nofilled lt black linewidth 2.000 dashtype solid
unset style line
unset style arrow
unset object
set style textbox transparent margins  1.0,  1.0 border
unset logscale
set offsets 0, 0, 0, 0
set parametric
set decimalsign '.'
set view 29, 47, 1, 1
set view  equal xyz
set samples 64, 64
set isosamples 21, 21
set surface 
unset contour
set cntrlabel  format '%8.3g' font '' start 5 interval 20
set mapping cartesian
set datafile separator whitespace
set hidden3d front offset 1 trianglepattern 3 undefined 1 altdiagonal bentover
set size ratio 0 1,1
set origin 0,0
set style data points
set style function lines
set urange [ -180.000 : 180.000 ] noreverse nowriteback
set vrange [ 0.00000 : 360.000 ] noreverse nowriteback
set xlabel "S_1" 
set ylabel "S_2" 
set zlabel "S_3" 
set xrange [-1.05:1.05]
set yrange [-1.05:1.05]
set zrange [-1.05:1.05]
set pm3d implicit at s
set pm3d depthorder  hidden3d 1
set pm3d interpolate 1,1 flush begin noftriangles noborder corners2color mean
set palette positive nops_allcF maxcolors 0 gamma 1.5 gray
set colorbox vertical origin screen 0.9, 0.2, 0 size screen 0.05, 0.6, 0 front bdefault
unset colorbox
set style boxplot candles range  1.50 outliers pt 7 separation 1 labels auto unsorted
# coordonnes ux,uy,uz du mode propre en fonction de teta et de tilt
ux(teta,tilt)=cos(2*teta)*cos(2*tilt)
uy(teta,tilt)=cos(2*teta)*sin(2*tilt)
uz(teta,tilt)=sin(2*teta)
# rotation de psi autour de u
S1(s1,s3,psi)=s1*(ux(teta,tilt)*ux(teta,tilt)*(1-cos(psi))+cos(psi))\
+s3*(ux(teta,tilt)*uz(teta,tilt)*(1-cos(psi))+uy(teta,tilt)*sin(psi))
S2(s1,s3,psi)=s1*(ux(teta,tilt)*uy(teta,tilt)*(1-cos(psi))+uz(teta,tilt)*sin(psi))\
+s3*(uy(teta,tilt)*uz(teta,tilt)*(1-cos(psi))-ux(teta,tilt)*sin(psi))
S3(s1,s3,psi)=s1*(ux(teta,tilt)*uz(teta,tilt)*(1-cos(psi))-uy(teta,tilt)*sin(psi))\
+s3*(uz(teta,tilt)*uz(teta,tilt)*(1-cos(psi))+cos(psi))

bind "t" "tilt=tilt-1;replot"
bind "T" "tilt=tilt+1;replot"
bind "d" "teta=teta-10;replot"
bind "D" "teta=teta+10;replot"
bind "c" "psi=psi-10;set vrange [0:psi];replot"
bind "C" "psi=psi+10;set vrange [0:psi];replot"
bind "s" "teta=teta-1;replot"
bind "S" "teta=teta+1;replot"
bind "x" "psi=psi-1;set vrange [0:psi];replot"
bind "X" "psi=psi+1;set vrange [0:psi];replot"
bind "w" "system('ST2stokes.py '.lignes.fichier);\
angles=system('ST2teta.py '.fichier);rep"
bind "f" "outp=system('Fitstokes.py '.fichier);\
	teta=1*word(outp,1);psi=1*word(outp,2);tilt=1*word(outp,3);\
	set vrange [0:psi];set arrow 7 from rmp*ux(teta,tilt),rmp*uy(teta,tilt),rmp*uz(teta,tilt) to\
 -rmp*ux(teta,tilt),-rmp*uy(teta,tilt),-rmp*uz(teta,tilt) \
heads lt 1;rep"


u = 0.0
