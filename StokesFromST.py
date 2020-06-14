#!/usr/bin/python
# -*-coding:Utf-8 -*

import numpy as np
from numpy import pi,cos,sin
import glob
#from scipy.optimize import least_squares

np.set_printoptions(precision=3)  # For compact display.

class Stokes:
    """ Classe définie par une liste de profils de Stokes
    enregistrés sous la forme ST<angle en deg>.
    Usage:
        import StokesFromST as ps
        cl=ps.Stokes()
        cl
        cl.VersStokes(l1=500,l2=600,fich="stokes")
        # => genere le fichier stokes  entre l1 et l2 en pixel
        # par defaut sur FWHM
        
        cl.Pixmax #indice du pic
        cl.Posmax #position du pic en micron
        cl.PixFWHM # diametre a 1/2 en pixel
        cl.FWHM # diametre a 1/2 en micron
    """
    def __init__(self):
        self.fichangle={} #dictionnaire fichier[angle (rad)]
        Lespeaks=np.zeros((1)) # numpy des indices de peak
        Lesrayons=np.zeros(1)  # numpy des rayons
        for fichier in glob.glob('ST*'):#liste des fichiers
            # fichier
            data=np.loadtxt(fichier)
            angle=float(fichier[2:])*pi/180
            self.fichangle[angle]=fichier
            #on prend la derniere colonne
            y=data[:,4:]
            Nmax=np.argmax(y)
            Imax=y[Nmax]
            N1=np.argmax(y[Nmax+1:]<Imax/2.)
            Lesrayons=np.hstack((Lesrayons,N1))
            Lespeaks=np.hstack((Lespeaks,[np.argmax(y)]))
        self.Pixmax=int(np.mean(Lespeaks[1:]))
        self.PixFWHM=int(np.mean(Lesrayons[1:]))
        self.FWHM=self.PixFWHM*4.4*2
        self.Posmax=self.Pixmax*4.4
    


    def __repr__(self):
        """ Affichage cool """
        reponse="-"*20+"\n"
        interf="\n"+reponse
        reponse+="Liste de fichiers:\n"
        for angle in sorted(self.fichangle):
            reponse+=self.fichangle[angle]
            reponse+=" "
        interf="\n"+reponse
        reponse+="\nPixMax={0}, PixFWHM={1}".format(self.Pixmax,self.PixFWHM) 
        reponse+="\nPosMax={0}micr, FWHM={1}micr\n".format(self.Posmax,self.FWHM) 
        return reponse
    
    def VersStokes(self,l1=1,l2=1,fich="stokes"):
        """
            genere le fichier stokes  entre l1 et l2 en pixel
            parcours la liste des ST*, et moyenne les Si dans
            la gamme [l1:l2]
            enregistre le fichier sous la forme
            init    => mesure
            S1 S2 S3  S0 S1 S2 S3
            la valuer init est extraite de l'ange du nom du fichier
        """
        #mise a jour des fichiers
        self.fichangle={} #dictionnaire fichier[angle (rad)]
        for fichier in glob.glob('ST*'):#liste des fichiers
            # fichier
            data=np.loadtxt(fichier)
            angle=float(fichier[2:])*pi/180
            self.fichangle[angle]=fichier
        if l1<2:
            l1=int(self.Pixmax-0.5*self.PixFWHM)
        if l2<2:
            l2=int(self.Pixmax+0.5*self.PixFWHM)
        Outdata=np.zeros((7))
        for angle in sorted(self.fichangle):
            # S1,S2,S3
            inStokes=np.array([cos(angle),0,sin(angle)])
            # fichier
            data=np.loadtxt(self.fichangle[angle])
            #on prend les bonnes lignes sans la derniere colonne
            subdata=data[l1:l2,:4]
            moyenne=np.mean(subdata,axis=0)
            Laligne=np.hstack((inStokes,moyenne))
            Outdata=np.vstack((Outdata,Laligne))
        np.savetxt(fich,Outdata[1:,:],fmt='%.2e',header='S1 S2 S3 =>S0 S1 S2 S3')
