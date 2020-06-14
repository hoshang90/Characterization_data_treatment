#!/usr/bin/python3
from time import sleep
import numpy as np
import PR50CC # lame L/4
import BS       # Babinet Soleil
from sys import exit

# ports serie: python3 -m serial.tools.list_ports
#/dev/ttyUSB2

#matplotlib.pyplot imsave 

from pydc1394 import Camera

class CameraPolar:
    """ Cartographie de la polarisation
    import
    ClassAcquisitionStokesCamera;cp=ClassAcquisitionStokesCamera.CameraPolar()
        1- pensez aux zero du BS et lame l/4
        2- cp.bs.VaLbda(valeur)
        3-cp.Mesure(attente=1,fich="lesimages",Npas=37,pas=10)
         => enregistre les Npas+1 images pour l'angle de la L/4
         entre 0, pas, 2*pas ,... Npas*pas 
    """
    def __init__(self) :
        F201B=2892819673575448
        # ------ Initialisation de la camera
        self.cam0=Camera(guid=F201B) 
        #lemodel=cam.model.decode()[-5:]
        self.l4=PR50CC.rotation()
        print("L4 ok")
        self.bs=BS.BabSoleil()
        print("BS ok")
        self.LHcamera()
        print("LxH={}x{}".format(self.Larg,self.Haut))

    def __repr__(self):
        """ Affichage cool """
        reponse="-"*20+"\n"
        reponse+="*----- Lambda/4:\n"
        reponse+="cp.l4.VaPos(-64.15);cp.l4.Zero() \n"
        reponse+="*----  Babinet soleil\n"
        reponse+="Pos. en fraction de lbda: cp.bs.VaLbda(0.) \n"
        reponse+=" Pour initialiser 0lbda et 1lbda du BS, voir BS.py \n"
        reponse+="cp.bs.Litpos()= {0} mm \n".format(self.bs.LitPos())
        reponse+="cp.bs.LitLbda()= {} Lbda \n".format(self.bs.LitLbda())
        reponse+="0lambda (cp.bs.ZeroLbda): {}\n".format(self.bs.ZeroLbda)
        reponse+="1lambda (cp.bs.UnLbda): {}\n".format(self.bs.UnLbda)
        reponse+="LxH= <--cp.LHcamera(): "
        reponse+="-"*20+"\n"
        reponse+='Usage: \n cp.Mesure(attente=1,fich="lesimages",Npas=37,pas=10)'
        reponse+="Traitement des data via: ClassTraitStokesCamera"
        return reponse


    
    def LHcamera(self) :
        """ return hauteur et largeur """
        self.cam0.start_capture()
        self.cam0.start_one_shot()
        frame = self.cam0.dequeue()
        (self.Larg,self.Haut)=frame.shape
        frame.enqueue()
        self.cam0.stop_one_shot()
        self.cam0.stop_capture()
        return (self.Larg,self.Haut)


    def Mesure(self,attente=1,fich="lesimages",Npas=37,pas=10) :
        self.l4.VaPos(0)
        self.LHcamera() # on verifie hauteur et largeur

        #-- initialisation des data: empilement des images 
        #ds un tableau 3D
        lesdata=np.zeros((Npas+1,self.Larg,self.Haut),\
                              dtype=np.uint16)
        Npixel=self.Larg*self.Haut
            # ------ informations dans le premier tableau
            #parametres de Stokes de l'entree
        phase=self.bs.LitLbda()*2*np.pi #phase du BS
        lesdata[0,0,0]= 65535  #S0
        lesdata[0,1,0]=int( (1+np.cos(phase))*32767) #S1
        lesdata[0,2,0]= 0  #S2
        lesdata[0,3,0]=int( (1+np.sin(phase))*32767) #S3
            #pas en "degree x 10"
        lesdata[0,0,1]=int(pas*10)
            #phase BS en frac de lambda
        lesdata[0,0,2]=int(self.bs.LitLbda()*65535)
        # ----- on démarre l'acquisition :
        self.cam0.start_capture()
        for i in range (Npas):
            x=self.l4.VaPos(pas*i)
            sleep(attente)
            self.cam0.start_one_shot()
            frame = self.cam0.dequeue()
            lesdata[i+1,:,:]=frame.copy()
            Nsat=(lesdata[i+1,:,:]>50000).sum()
            print("Frame number ({}) has {:.2f}% ({}pixels) au dessus de 50 milles ".format(i+1,Nsat/Npixel*100,Nsat))
            if Nsat>0.05*Npixel :
                print("!!! Attention {} pixels au dessus de 50 milles ".format(Nsat))
                self.cam0.stop_one_shot()
                self.cam0.stop_capture()
                exit(0)

            frame.enqueue()
            self.cam0.stop_one_shot()
        self.cam0.stop_capture()

        np.save(fich,lesdata)
        #comme on a fait un tour, on peut remettre la L/4 à zero :
        self.l4.VaPos(360)
        self.l4.Zero()
        return 1

