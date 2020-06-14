
#!/usr/bin/python3
from time import process_time
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import glob

from struct import pack  
from matplotlib.pyplot import imsave

# ports serie: python3 -m serial.tools.list_ports
#/dev/ttyUSB2

#matplotlib.pyplot imsave 


class Stokes :

    """ Cartographie de la polarisation
    import ClassTraitStokesCamera;st=ClassTraitStokesCamera.Stokes()
         
    """
    def __init__(self) :
        print("ok")
        self.__repr__()

    def __repr__(self):
        """ Affichage cool """
        reponse="-"*20+"\n"
        reponse += "\n" + 'To find position of the guided mode and dimensions of the rectangle:' + "\n"
        reponse += "st.Pos_max(fich='lesimages.npy',frame_numb=12, x_range=50, y_range=50)" + "\n"
        reponse += "\n" + 'To save stocks parameters values in file:' + "\n"
        reponse += "st.Save_stocks(fich='lesimages.npy',frame_numb=12, x_range=50, y_range=50)" + "\n"
        reponse += "\n"
        reponse+=" Moyenne des S dans un rectange:\n"
        reponse+='st.Moy(fich="lesimages.npy",bdf=70,x1=50,y1=50,Lx=30,Ly=30)'
        reponse+="\nSi Lx*Ly=0, toute l'image\n"
        reponse += "\n"
        reponse+=" Cartograhpie:\n "
        reponse+='st.Carto(fich="lesimages.npy",bdf=70,x1=50,y1=50,Lx=30,Ly=30)'
        reponse+="\n"+'puis st.Sauve(fich="res")'+"\n"
        reponse+="-"*20+"\n"
        return reponse

    #------------------------------------------------
    def func(self,x,S0,S1,S2,S3):
        sindelta=1
        cosdelta=0
        a=S1/2.+S1/2*np.cos(4*x)
        b=S2/2*np.sin(4*x)
        return S0+a+b-S3*np.sin(2*x)*sindelta
    #------------------------------------------------
    def Moy(self,fich="lesimages.npy",bdf=70,x1=-1,y1=-1,Lx=0,Ly=0) :
        """ Stokes apres avoir moyenner les intensités dans le rectangle """
        #--- on lit le debut du fichier pour le pas:
        Fulldata = np.load(fich)
        Npas = Fulldata.shape[0]
        x_range=Lx/2;y_range=Ly/2
        lesdata=np.load(fich)[0,0:5,0:5]
        pas=lesdata[0,1]/10.
        bs=lesdata[0,2]/65535.
        # Sin:
        Sin1=lesdata[1,0]/32767.-1
        Sin3=lesdata[3,0]/32767.-1
        print("S=({:.2f},0.00,{:.2f})".format(Sin1,Sin3))
        if (Lx*Ly>0):
            lesdata = np.load(fich)[:, x1:x1 + Lx, y1:y1 + Ly]
            for frame_numb in range(1, Npas):
                x1, y1 = np.unravel_index(np.argmax(Fulldata[frame_numb,:,:], axis=None), Fulldata[frame_numb,:,:].shape)
                x1=x1-x_range;y1=y1-y_range
                print("x1 is {} and y1 = {}".format(x1,y1))
                lesdata[frame_numb,:,:]=Fulldata[frame_numb,int(x1):int(x1+Lx),int(y1):int(y1+Ly)]
        else :
            lesdata=np.load(fich)
        (Npas,Larg,Haut)=lesdata.shape
        self.lesdata=lesdata
        Npas=Npas-1
        Yexp=np.mean(lesdata[1:,:,:],axis=(1,2))
        Xexp=np.radians(np.arange(0,Npas*pas,pas))
        Sinus2=np.sin(Xexp*2)
        Sinus4=np.sin(Xexp*4)
        Cos4=np.cos(Xexp*4)

        m0=np.mean(Yexp)
        # calcul simple
        S3=-2*np.mean(Yexp*Sinus2)
        S2=4*np.mean(Yexp*Sinus4)
        S1=4*np.mean(Yexp*Cos4)
        S0=m0-0.5*S1
        #print("Estimation: S0={:.1f},  S1={:.2f}, S2={:.2f}, S3={:.2f}".format(S0,S1/S0,S2/S0,S3/S0))
        # fit
        popt,pcov = curve_fit(self.func,Xexp,Yexp, p0=[S0,S1,S2,S3])
        (S0,S1,S2,S3)=popt
        DOP=np.sqrt(S1**2+S2**2+S3**2)/S0
        #length of the polarized part of the light
        PL=np.sqrt(S1**2+S2**2+S3**2)
        print("Fit S0={:.1f}, S1={:.2f}, S2={:.2f}, S3={:.2f}".format(1./DOP,S1/S0,S2/S0,S3/S0))
        ecc=S3/(S0+np.sqrt(S1*S1+S2*S2))
        ori=0.5*np.arctan2(S2,S1)*57.296
        print("ecc={:.2f}, orientation={:.2f}".format(ecc,ori))
        print("DOP: {:.2f}".format(DOP) )
        return(Sin1,0,Sin3,DOP,S1/PL,S2/PL,S3/PL)

    def Pos_max(self,fich="lesimages.npy",frame_numb=12, x_range=50, y_range=50):
        """ Finds position of the maximum value pixel in a defined frame then
        it plots a rectangle with max value center and x_range and y_range number of pixels
         in all directions"""
        ledata = np.load(fich)
        frame=ledata[frame_numb,:,:]
        x1, y1 = np.unravel_index(np.argmax(frame, axis=None), frame.shape)
        print("The position of maximum point is: \n X={} and Y={}".format(x1,y1))
        Lx=2*x_range
        Ly=2*y_range
        print("The plotted image has specs \n x1={}, y1={}, Lx={}, Ly={}".format(x1,y1,Lx,Ly)) 
       # print("st.Moy(fich=fich,x1=x1,y1=y1,Lx=Lx,Ly=Ly)".format())
       #  self.Moy(fich=fich,x1=int(x1),y1=int(y1),Lx=int(Lx),Ly=int(Ly))
        plt.imshow(frame[int(x1-x_range):int(x1+x_range),int(y1-y_range):int(y1+y_range)], cmap="nipy_spectral")
        plt.colorbar()
        plt.show()
    def Save_stocks(self,fich="lesimages.npy",frame_numb=12, x_range=50, y_range=50):
        """ Finds position of the maximum value pixel in a defined frame then
        it plots a rectangle with max value center and x_range and y_range number of pixels
         in all directions"""
        ledata = np.load(fich)
        frame = ledata[frame_numb, :, :]
        x1, y1 = np.unravel_index(np.argmax(frame, axis=None), frame.shape)
        print("The position of maximum point is: \n X={} and Y={}".format(x1, y1))
        Lx = 2 * x_range
        Ly = 2 * y_range
        print("The plotted image has specs \n x1={}, y1={}, Lx={}, Ly={}".format(x1, y1, Lx, Ly))
        plt.imshow(frame[int(x1-x_range):int(x1+x_range),int(y1-y_range):int(y1+y_range)], cmap="nipy_spectral")
        plt.colorbar()
        plt.show()
        print("--------------")
        stokesVector=np.zeros((1,7))
        for lesimages in (glob.glob('lambda*.npy')):
            print(lesimages)
            x1,y1=np.unravel_index(np.argmax(frame, axis=None), frame.shape)
            x1=x1-x_range;y1=y1-y_range
            ret=self.Moy(fich=lesimages,x1=int(x1),y1=int(y1),Lx=int(Lx),Ly=int(Ly))
            stokesVector=np.vstack((stokesVector,ret))
        np.savetxt("stokes",stokesVector[1:,],fmt='%.3f')

    def Carto(self,fich="lesimages.npy",bdf=70,x1=-1,y1=-1,Lx=0,Ly=0) :
        """ Recupère le fichier puis applique sur chaque pixel le fit
            * cp.tabS[0-3]: les parametres de Stokes
            * cp.DOP : le degree of Polarization
        """
        #--- on lit le debut du fichier pour le pas:
        lesdata=np.load(fich)[0,0:5,0:5]
        pas=lesdata[0,1]/10.
        bs=lesdata[0,2]/65535.
        # Sin:
        S1=lesdata[0,1]/32767.-1
        S3=lesdata[0,3]/32767.-1
        print("S=({:.2f},0.00,{:.2f})".format(S1,S3))
        print("pas={}".format(pas))

        if (Lx*Ly>0) :
            lesdata=np.load(fich)[:,x1:x1+Lx,y1:y1+Ly]
        else :
            lesdata=np.load(fich)
        (Npas,Larg,Haut)=lesdata.shape
        self.lesdata=lesdata
        Npas=Npas-1

        self.tabS0=np.zeros((Larg,Haut),dtype=np.uint16)
        self.DOP=np.zeros((Larg,Haut))
        self.tabS1=np.zeros((Larg,Haut))
        self.tabS2=np.zeros((Larg,Haut))
        self.tabS3=np.zeros((Larg,Haut))

        Xexp=np.radians(np.arange(0,Npas*pas,pas))
        Sinus2=np.sin(Xexp*2)
        Sinus4=np.sin(Xexp*4)
        Cos4=np.cos(Xexp*4)

        for i in range(Larg):
            t0= process_time()
            for j in range(Haut):
                Yexp=lesdata[1:,i,j].astype(float)-bdf
                # on ne calcul que si le signal >1.1*Bdf
                m0=np.sum(Yexp)/Npas
                if (abs(m0)<1.1*bdf):
                    (S0,S1,S2,S3)=(1,0,0,0)
                else :
                    # calcul simple
                    S3=-2*np.sum(Yexp*Sinus2)/Npas
                    S2=4*np.sum(Yexp*Sinus4)/Npas
                    S1=4*np.sum(Yexp*Cos4)/Npas
                    S0=m0-0.5*S1
                    # fit 
                    (S0,S1,S2,S3),pcov = curve_fit(self.func,Xexp,Yexp, p0=[S0,S1,S2,S3])

                self.tabS0[i,j]=np.uint16(S0)
                self.DOP[i,j]=np.sqrt(S1**2+S2**2+S3**2)/S0
                self.tabS1[i,j]=S1/S0
                self.tabS2[i,j]=S2/S0
                self.tabS3[i,j]=S3/S0
            te=process_time()-t0
            if (i%27 == 0) :
                print("Boucle {:.2f}, reste \
                                {:.2f}min".format(te,te*(Larg-i)/60))
        return 1

    def Bornes(self,x) :
        if x > 127 :
            retour=127
        elif x<-128 :
            retour=-128
        else :
            retour =x
        return retour
            
    def Sauve(self,fich="res") :
        """ Differentes sauvegardes :
            * fichS[0..3].npy: les tableaux en python
            * fichS0.png  -> 8 bits
            * fich100x100_Stokes.bin : 
                -> les dimensions de la matrice : LargxHaut
                -> les quatres Si et DOP en format binaires Hbbbb
            * fich100x100_Ellip.bin : 
                -> les dimensions de la matrice : LargxHaut
                -> ecc et inclinaison en float binaires ff
            """
        (Larg,Haut)=self.tabS0.shape
        #format python
        np.save(fich+"S0",self.tabS0)
        np.save(fich+"S1",self.tabS1)
        np.save(fich+"S2",self.tabS2)
        np.save(fich+"S3",self.tabS3)

        #image 8 bits pour S0:
        imsave(fich+"S0.png",self.tabS0,cmap="gray")

        # ---------------
        # fichiers binaires des parametres de Stokes pour gnuplot :
        #set cbrange [-1:1]
        NomfichS=fich+"{:0>4}x{:0>4}_Stokes.bin".format(Haut,Larg)
        fichbinaire=open(NomfichS,"wb")
        for i in range(Larg):
            for j in range(Haut):
                s0=self.tabS0[i,j]
                s1=self.Bornes(int(self.tabS1[i,j]*127))
                s2=self.Bornes(int(self.tabS2[i,j]*127))
                s3=self.Bornes(int(self.tabS3[i,j]*127))
                dop=self.Bornes(int(self.DOP[i,j]*127))
                fichbinaire.write(pack("Hbbbb",s0,s1,s2,s3,dop))
        fichbinaire.close()
        
        #---  fichier binaire ellipse de polarisation ----
        #-- ! verifier le retour du write 
        #-- Hff => 12bits au lieu de 10
        NomfichE=fich+"{:0>4}x{:0>4}_Ellip.bin".format(Haut,Larg)
        fichbinaire=open(NomfichE,"wb")

        ecc=self.tabS3/(1+np.sqrt(self.tabS1**2+self.tabS2**2))
        rx=np.cos(np.arctan(ecc))*(self.tabS0>1)
        ry=np.abs(np.sin(np.arctan(ecc)))
        incli=0.5*np.arctan2(self.tabS2,self.tabS1)*57.296
        sens=np.sign(self.tabS3)
        for i in range(Larg):
            for j in range(Haut):
                ix=int(rx[i,j]*250)
                iy=int(ry[i,j]*250)
                a=int(incli[i,j])
                s=int(sens[i,j]+5)
                fichbinaire.write(pack("BBhB",ix,iy,a,s))
        fichbinaire.close()
        #--------------------------
        self.AideGnuplot(NomfichS,NomfichE,Larg,Haut)



    def AideGnuplot(self,NomfichS,NomfichE,Larg,Haut):
        """ Aide pour afficher les fichiers binaires dans gnuplot """

        print("----\n -Pour afficher  l'image de S0 dans gnuplot: \n ")
        print("spl \""+NomfichS+"\" binary format=\"%uint16%*4int8\"\\")
        print(" array=({},{})  w image ".format(Larg,Haut))
        print("----\n -Pour afficher  l'image de dop dans gnuplot: \n")
        print("spl \""+NomfichS+"\" binary format=\"%uint16%4int8\"\\")
        print(" array=({},{}) u ($5/127) flipy w image ".format(Larg,Haut))
        # ---------------
        print("----\n -Pour afficher  la carto des ellipses dans gnuplot")
        print("     au dessus de S0:\n")
        print("set multiplot")
        print("ray=60") #rayon ellipse
        print("set linetype 4 lc rgb \"red\"")
        print("set linetype 6 lc rgb \"green\"")
        print("spl \""+NomfichS+"\" binary format=\"%uint16%*4int8\"\\")
        print(" array=({},{})  w image ".format(Larg,Haut))
        print("pl \""+NomfichE+"\" binary format=\"%2uint8%int16%uint8\" ")
        print("array=({},{}) \\ ".format(Larg,Haut))
        print("flipy  u  ($1/ray):($2/ray):3:4 w ellipse lc variable")





        




        


