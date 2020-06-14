#!/usr/bin/python3
# -*-coding:Utf-8 -*
import sys,getopt
import StokesFromST as ps

x=ps.Stokes()
x.VersStokes(l1=int(sys.argv[1]),l2=int(sys.argv[2]),fich=sys.argv[3])
