#!/usr/bin/python3
# -*-coding:Utf-8 -*
import  time
import numpy as np
import BS
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
w0=80

bs=BS.BabSoleil()
           
cam.start_capture()
Npts=70
step=0.001
AngleStart=0.21
data=np.zeros((Npts,2))
bs.VaLbda(AngleStart)
time.sleep(0.2)

for i in range(Npts):
    #capture une frame et la copy dans CamArray
    bs.VaLbda(AngleStart+i*step)
    time.sleep(0.2)
    cam.start_one_shot()
    frame =cam.dequeue()
    CamArray = frame.copy()
    frame.enqueue()
    cam.stop_one_shot()
    # on recupere les info de la camera
    data[i,0]=AngleStart+i*step
    data[i,1]=CamArray.sum()

np.savetxt("BS_find_L0_zero",data)
