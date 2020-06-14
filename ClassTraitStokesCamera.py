
#!/usr/bin/python3
from time import process_time
import sys
import numpy as np
from scipy import optimize
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import glob
from PIL import Image
from io import BytesIO

from struct import pack  
from matplotlib.pyplot import imsave
import matplotlib.animation as animation ###############
import imageio #####################

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
        reponse = "-"*20+"\n"
        reponse += "Moyenne des S dans un rectange:\n"
        reponse += 'st.Moy(fich="lambda0.npy",bdf=70,x1=-1,y1=-1,Lx=0,Ly=0,show_image=False,frame_numb=12, anime=False,save_gif=False)'
        reponse += "\nSi Lx*Ly=0, toute l'image\n"
        reponse += "The parameters--> show_image is to show the image of the analysed area by choosing a frame from frame_numb parameter," \
                   " anime is to animate all the frames of the file, and save_gif is to save a gif file with the name of the file )\n"+"\n"
        reponse += 'To choose the right position of the guided mode and dimensions of the rectangle then find' \
                          'Stokes parameters, run:' + "\n"
        reponse += 'st.Moy_choose(fich="lambda0.npy",frame_numb=12,show_image=True, anime=False,save_gif=False)\n'
        reponse += "\n" + 'To save Stokes parameters values in a file called Stokes by choosing the exact postion of the guided mode, run:\n'
        reponse += 'st.Save_Stokes_choose(fich="lambda0.npy",frame_numb=12,show_image=False, anime=False, save_gif=False)\n'
        reponse += 'The Stokes parameters are calculated and saved in the file from the .npy files saved in the directory\n'
        reponse += '!!!!! please be aware of that the .npy files should be saved as lambda0.npy, lambda0p25.npy, and lamabda1.npy etc...\n'
        reponse += "\n" + 'To find position of the guided mode and dimensions of the rectangle, run: \n'
        reponse += 'st.Pos_max(fich="lambda0.npy",frame_numb=12, x_range=50, y_range=50)\n'
        reponse += "\n" + 'To save Stokes parameters values in a file called Stokes based on the Pos_max function, run:\n'
        reponse += "st.Save_Stokes(fich='lambda0.npy',frame_numb=12, x_range=50, y_range=50)\n"
        reponse += "\n" +" Cartograhpie:\n"
        reponse += 'st.Carto(fich="lambda0.npy",bdf=70,x1=50,y1=50,Lx=30,Ly=30)'
        reponse += "\n"+'puis st.Sauve(fich="res")'+"\n"
        reponse += "-"*20+"\n"
        return reponse

    #------------------------------------------------
    def func(self,x,S0,S1,S2,S3):
        sindelta=1
        cosdelta=0
        a=S1/2.+S1/2*np.cos(4*x)
        b=S2/2*np.sin(4*x)
        return S0+a+b-S3*np.sin(2*x)*sindelta
    #------------------------------------------------
    def rot_diff(self, param, vstokes): # this function is necessary for the calculation of S3, it is taken from Fit2
        """
        Stokes(tourné)-Stokes(Init)
        Stokes(tourné): rotation autours du mode propre de psi
        mode propre= u definit ci dessous
        """
        t0, psi, tilt = param
        # coordonnes ux,uy,uz du mode propre en fonction de teta et de tilt
        ux = np.cos(2 * t0) * np.cos(2 * tilt)
        uy = np.cos(2 * t0) * np.sin(2 * tilt)
        uz = np.sin(2 * t0)
        # rotation de psi autour de u=(ux,uy,uz)
        S1 = vstokes[:, 0] * (ux * ux * (1 - np.cos(psi)) + np.cos(psi))
        S1 += vstokes[:, 2] * (ux * uz * (1 - np.cos(psi)) + uy * np.sin(psi))

        S2 = vstokes[:, 0] * (ux * uy * (1 - np.cos(psi)) + uz * np.sin(psi))
        S2 += vstokes[:, 2] * (uy * uz * (1 - np.cos(psi)) - ux * np.sin(psi))

        S3 = vstokes[:, 1] * (ux * uz * (1 - np.cos(psi)) - uy * np.sin(psi))
        S3 += vstokes[:, 2] * (uz * uz * (1 - np.cos(psi)) + np.cos(psi))

        diff = np.column_stack((S1, S2, S3)) - vstokes[0:, 4:]
        # le ravel met a plat le tableau
        return (diff.ravel())
    #------------------------------------------------
    def Moy(self,fich="lambda0.npy",bdf=70,x1=-1,y1=-1,Lx=0,Ly=0,show_image=False,frame_numb=12, anime=False,save_gif=False,save_colored_gif=False): ###################
        """ Stokes apres avoir moyenner les intensités dans le rectangle """
        #--- on lit le debut du fichier pour le pas:
        lesdata=np.load(fich)[0,0:5,0:5]
        pas=lesdata[0,1]/10.
        bs=lesdata[0,2]/65535.
        # Sin:
        Sin1=lesdata[1,0]/32767.-1
        Sin3=lesdata[3,0]/32767.-1
        print("S=({:.2f},0.00,{:.2f})".format(Sin1,Sin3))
        if (Lx*Ly>0) :
            lesdata=np.load(fich)[:,x1:x1+Lx,y1:y1+Ly]
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
        if show_image==True:###################
            plt.imshow(lesdata[frame_numb,:,:],cmap="nipy_spectral")
            plt.clim(0, 55000)
            #plt.colorbar()
            plt.title("This is the analysed part of the frames")
            plt.show()
        if anime==True:
            ims = []
            fig=plt.figure()
            for i in range(1,lesdata.shape[0]):
                #plt.title(" {}".format(i))
                im = plt.imshow(lesdata[i, :, :], cmap="nipy_spectral", animated=True)
                plt.clim(0, 55000)
                # newpng[i]=im.mtplot2png
                ims.append([im])
            ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True,repeat_delay=500)
            # ani.save(fich.replace(".npy",".gif")) #######there is a bug in matplotlib, we wait until fix
            plt.show(block=False)
        if save_gif==True:
            writer = imageio.get_writer(fich.replace(".npy", ".gif"))
            for i in range(1, lesdata.shape[0]):
                writer.append_data(np.uint8(lesdata[i] / 2 ** 8))
              #  writer.append_data(newpng[i])
            writer.close()###########################
        if save_colored_gif == True:
            images = []
            plt.axis('off')
            for i in range(1, lesdata.shape[0]):
                plt.imshow(lesdata[i, :, :], cmap="nipy_spectral")
                plt.clim(0, 55000)
                # Save it to a temporary buffer.
                buf = BytesIO()
                plt.savefig(buf, bbox_inches='tight', pad_inches=0)
                images.append(Image.fromarray(np.array(Image.open(buf))))# It can only be saved if it is in the format of PIL
                print("Process running in frame number {}".format(i))
            images[0].save(fich.replace(".npy", ".gif"), save_all=True, append_images=images[1:], optimize=False,
                           loop=0)# from an example to save gif file from list of figure in PIL module
            plt.axis("on")
        return(Sin1,0,Sin3,DOP,S1/PL,S2/PL,S3/PL) 

    def Moy_choose(self,fich="lambda0.npy",frame_numb=12,show_image=True, anime=False,save_gif=False,save_colored_gif=False):###################
        """ It asks user to choose position of x1, y1, Lx, and then it
        calculates Stokes parameters by using Moy function"""
        ledata = np.load(fich)
        frame = ledata[frame_numb, :, :]
        fig, ax = plt.subplots()
        ax.imshow(frame,cmap="nipy_spectral")
        cursor = Cursor(ax)
        fig.canvas.mpl_connect('motion_notify_event', cursor.mouse_move)
        # print("Please click on x1 value")
        # ginput(n=1, timeout=30, show_clicks=True, mouse_add=1, mouse_pop=3, mouse_stop=2)
        plt.title("Please choose the position of x1 and y1")
        xy_index = plt.ginput(n=1, show_clicks=True)
        xy_index = np.asarray(xy_index);
        xy_index = xy_index.transpose()
        x1= int(xy_index[0]);y1=int(xy_index[1])
        plt.axvline(x=x1, linewidth=1,color="w")
        plt.axhline(y=y1, linewidth=1,color="w")
        print("x1 is",x1)
        print("y1 is",y1)
        plt.title("Please choose the position of x2 and y2")
        xy_index = plt.ginput(n=1, show_clicks=True)
        xy_index = np.asarray(xy_index);
        xy_index = xy_index.transpose()
        x2 = int(xy_index[0]) 
        y2 = int(xy_index[1])
        Lx = np.absolute(x2 - x1)
        Ly = np.absolute(y2 - y1)
        print("Lx is",Ly)
        print("Ly is",Lx)
        plt.close()
        print("The plotted image has specs \n x1={}, y1={}, Lx={}, Ly={}".format(x1, y1, Lx, Ly))
        self.Moy(fich=fich, x1=y1, y1=x1, Lx=Ly,Ly=Lx,show_image=show_image,frame_numb=frame_numb, anime=anime,
                 save_gif=save_gif, save_colored_gif=save_colored_gif)
        
    def Save_Stokes_choose(self,fich="lambda0.npy",frame_numb=12,show_image=False, anime=False, save_gif=False,save_colored_gif=False):##############
        """ It asks user to choose position of x1, y1, Lx, and then it
        saves Stokes parameters in file called Stokes by using Moy function """
        ledata = np.load(fich)
        frame = ledata[frame_numb, :, :]
        fig, ax = plt.subplots()
        ax.imshow(frame,cmap="nipy_spectral")
        cursor = Cursor(ax)
        fig.canvas.mpl_connect('motion_notify_event', cursor.mouse_move)
        # print("Please click on x1 value")
        # ginput(n=1, timeout=30, show_clicks=True, mouse_add=1, mouse_pop=3, mouse_stop=2)
        plt.title("Please choose the position of x1 and y1")
        xy_index = plt.ginput(n=1, show_clicks=True)
        xy_index = np.asarray(xy_index);
        xy_index = xy_index.transpose()
        x1= int(xy_index[0]);y1=int(xy_index[1])
        plt.axvline(x=x1, linewidth=1,color="w")
        plt.axhline(y=y1, linewidth=1,color="w")
        print("x1 is",x1)
        print("y1 is",y1)
        plt.title("Please choose the position of x2 and y2")
        xy_index = plt.ginput(n=1, show_clicks=True)
        xy_index = np.asarray(xy_index);
        xy_index = xy_index.transpose()
        x2 = int(xy_index[0]) 
        y2 = int(xy_index[1])
        Lx = np.absolute(x2 - x1)
        Ly = np.absolute(y2 - y1)
        print("Lx is",Lx)
        print("Ly is",Lx)
        plt.close()
        print("The plotted image has specs \n x1={}, y1={}, Lx={}, Ly={}".format(x1, y1, Lx, Ly))
        print("--------------")
        stokesVector=np.zeros((1,7))
        for lesimages in sorted(glob.glob('lambda*.npy')):
            print(lesimages)
            ret=self.Moy(fich=lesimages,x1=y1, y1=x1, Lx=Ly,Ly=Lx,show_image=show_image,frame_numb=frame_numb,
                         anime=anime, save_gif=save_gif, save_colored_gif=save_colored_gif)
            stokesVector=np.vstack((stokesVector,ret))
            plt.title(lesimages)            
        np.savetxt("Stokes",stokesVector[1:,],fmt='%.3f')#fich.replace(".npy", ".Stokes"
        ######## here i include the Fitstokes.py file
        data=stokesVector[1:,]
        x0 = [np.deg2rad(45), np.deg2rad(-45), 0]
        sol, flag = optimize.leastsq(self.rot_diff, x0, args=(data))
        print("teta is = {:.1f}, psi is = {:.1f}, and tilt={:.1f}".format(np.rad2deg(sol)[0], np.rad2deg(sol)[1], np.rad2deg(sol)[2]))
        S3 = np.array((np.sin(2*sol[0]),np.sin(sol[0])))
        print("S3 is = {:.3f}, {:.3f}".format(S3[0],S3[1]))

    def S3_from_Stokes(self,fich="Stokes"):#fich="lambda0.npy")
        '''This method calculates S3 from a file called Stokes, the file must include input and output Stokes parameters.
        this file can be saved from the method Save_Stokes_choose'''
        data = np.loadtxt("Stokes")#fich.replace(".npy", ".Stokes")
        x0 = [np.deg2rad(45), np.deg2rad(-45), 0]
        sol, flag = optimize.leastsq(self.rot_diff, x0, args=(data))
        print("teta is = {:.1f}, psi is = {:.1f}, and tilt={:.1f}".format(np.rad2deg(sol)[0], np.rad2deg(sol)[1], np.rad2deg(sol)[2]))
        S3 = np.array((np.sin(2*sol[0]),np.sin(sol[0])))
        print("S3 is = {:.3f}, {:.3f}".format(S3[0],S3[1])) #(np.sin(2 * sol[0])), np.sin(sol[0]))
        # lam=?????
        # print("The eign lambda of the eigen mode is = {:.3f}".format(lam))


    def Pos_max(self,fich="lambda0.npy",frame_numb=12, x_range=50, y_range=50):
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
        print("st.Moy(fich=fich,x1=x1,y1=y1,Lx=Lx,Ly=Ly)".format())
        self.Moy(fich=fich,x1=int(x1),y1=int(y1),Lx=int(Lx),Ly=int(Ly))
        plt.imshow(frame[int(x1-x_range):int(x1+x_range),int(y1-y_range):int(y1+y_range)], cmap="nipy_spectral")
        plt.colorbar()
        plt.show()
    def Save_Stokes(self,fich="lambda0.npy",frame_numb=12, x_range=50, y_range=50):
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
        for lesimages in sorted(glob.glob('lambda*.npy')):
            print(lesimages)
            x1,y1=np.unravel_index(np.argmax(frame, axis=None), frame.shape)
            x1=x1-x_range;y1=y1-y_range
            ret=self.Moy(fich=lesimages,x1=int(x1),y1=int(y1),Lx=int(Lx),Ly=int(Ly))
            stokesVector=np.vstack((stokesVector,ret))
        np.savetxt("stokes",stokesVector[1:,],fmt='%.3f')

    def Carto(self,fich="lambda0.npy",bdf=70,x1=-1,y1=-1,Lx=0,Ly=0,show_image=False,frame_numb=12, anime=False,save_gif=False, save_colored_gif=False) :
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
        if show_image==True:###################
            plt.imshow(lesdata[frame_numb,:,:],cmap="nipy_spectral")
            plt.clim(0, 55000)
            #plt.colorbar()
            plt.title("This is the analysed part of the frames")
            plt.show()
        if anime==True:
            ims = []
            fig=plt.figure()
            for i in range(1,lesdata.shape[0]):
                #plt.title(" {}".format(i))
                im = plt.imshow(lesdata[i, :, :], cmap="nipy_spectral", animated=True)
                plt.clim(0, 55000)
                # newpng[i]=im.mtplot2png
                ims.append([im])
            ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True,repeat_delay=500)
            # ani.save(fich.replace(".npy",".gif")) #######there is a bug in matplotlib, we wait until fix
            plt.show(block=True)
        if save_gif==True:
            writer = imageio.get_writer(fich.replace(".npy", ".gif"))
            for i in range(1, lesdata.shape[0]):
                writer.append_data(np.uint8(lesdata[i] / 2 ** 8))
              #  writer.append_data(newpng[i])
            writer.close()###########################
        if save_colored_gif == True:
            images = []
            plt.axis('off')
            for i in range(1, lesdata.shape[0]):
                plt.imshow(lesdata[i, :, :], cmap="nipy_spectral")
                plt.clim(0, 55000)
                # Save it to a temporary buffer.
                buf = BytesIO()
                plt.savefig(buf, bbox_inches='tight', pad_inches=0)
                images.append(Image.fromarray(np.array(Image.open(buf))))# It can only be saved if it is in the format of PIL
                print("Process running in frame number {}".format(i))
            images[0].save(fich.replace(".npy", ".gif"), save_all=True, append_images=images[1:], optimize=False,
                           loop=0)# from an example to save gif file from list of figure in PIL module
            plt.axis("on")
        return 1
    def Carto_choose(self,fich="lambda0.npy",bdf=70,frame_numb=12,show_image=False, anime=False,save_gif=False,save_colored_gif=False):###################
        """ It asks user to choose position of x1, y1, Lx, and then it
        calculates Stokes parameters by using Moy function"""
        ledata = np.load(fich)
        frame = ledata[frame_numb, :, :]
        fig, ax = plt.subplots()
        ax.imshow(frame,cmap="nipy_spectral")
        cursor = Cursor(ax)
        fig.canvas.mpl_connect('motion_notify_event', cursor.mouse_move)
        # print("Please click on x1 value")
        # ginput(n=1, timeout=30, show_clicks=True, mouse_add=1, mouse_pop=3, mouse_stop=2)
        plt.title("Please choose the position of x1 and y1")
        xy_index = plt.ginput(n=1, show_clicks=True)
        xy_index = np.asarray(xy_index);
        xy_index = xy_index.transpose()
        x1= int(xy_index[0]);y1=int(xy_index[1])
        plt.axvline(x=x1, linewidth=1,color="w")
        plt.axhline(y=y1, linewidth=1,color="w")
        print("x1 is",x1)
        print("y1 is",y1)
        plt.title("Please choose the position of x2 and y2")
        xy_index = plt.ginput(n=1, show_clicks=True)
        xy_index = np.asarray(xy_index);
        xy_index = xy_index.transpose()
        x2 = int(xy_index[0])
        y2 = int(xy_index[1])
        Lx = np.absolute(x2 - x1)
        Ly = np.absolute(y2 - y1)
        print("Lx is",Ly)
        print("Ly is",Lx)
        plt.close()
        print("The plotted image has specs \n x1={}, y1={}, Lx={}, Ly={}".format(x1, y1, Lx, Ly))
        self.Carto(fich=fich, x1=y1, y1=x1, Lx=Ly,Ly=Lx,show_image=show_image,frame_numb=frame_numb, anime=anime,
                 save_gif=save_gif, save_colored_gif=save_colored_gif)
        self.Sauve(fich="Carto") 

#####################################
    def Bornes(self,x) :
        if x > 127 :
            retour=127
        elif x<-128 :
            retour=-128
        else :
            retour =x
        return retour
#######################################
    def Sauve(self,fich="lambda") :
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
###########################################
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

#######################################
class Cursor(object):############# this class is necesary for the Cursor position plot in the ginput fucntion
    def __init__(self, ax):
        self.ax = ax
        self.lx = ax.axhline(linewidth=1,color='r')  # the horiz line
        self.ly = ax.axvline(linewidth=1,color='r')  # the vert line
        # text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)
    def mouse_move(self, event):
        if not event.inaxes:
            return
        x, y = event.xdata, event.ydata
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)
        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))#right x and y value in the plot
        self.ax.figure.canvas.draw()





        




        





        




        


