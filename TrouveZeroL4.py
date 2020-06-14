#!/usr/bin/python3
# -*-coding:Utf-8 -*
import  time
import numpy as np
import PR50CC
#from scipy.optimize import curve_fit

#--------------------------------
        # Les frames d'entrées
from pydc1394 import Camera
# la camera est appellée par son uid
#pour l'avoir: 
#from pydc1394.camera2 import Context
#for c in Context().cameras:
#    print(c)
#(2892819673481529, 0) => F146B
#(2892819673575448, 0) => F201B

#from FakeCamera import Camera
F201B=2892819673575448
guidCam=F201B
cam=Camera(guid=guidCam) 
lemodel=cam.model.decode()[-5:]
w0=8005
l4=PR50CC.rotation()
           
cam.start_capture()
Npts=50
step=0.1
AngleStart=85
data=np.zeros((Npts,2))
l4.VaPos(AngleStart)
time.sleep(0.5)

for i in range(Npts):
    #capture une frame et la copy dans CamArray
    l4.VaPos(AngleStart+i*step)
    time.sleep(0.2)
    cam.start_one_shot()
    frame =cam.dequeue()
    CamArray = frame.copy()
    frame.enqueue()
    cam.stop_one_shot()
    # on recupere les info de la camera
    data[i,0]=AngleStart+i*step
    data[i,1]=CamArray.mean()

np.savetxt("L4_find_zero",data)
