#!/usr/bin/python
# -*-coding:Utf-8 -*
import sys
import numpy as np
from numpy import pi,cos,sin
np.set_printoptions(precision=3)  # For compact display.
data=np.loadtxt(sys.argv[1])
   #on prend les bonnes  colonnes
s1=data[:,0]
s3=data[:,2]
teta=np.rad2deg(np.arctan2(s3,s1))
for angle in teta:
    print(angle)

