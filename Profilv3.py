#!/usr/bin/python3
# -*-coding:Utf-8 -*
import  time
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os, glob
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
style.use('ggplot')
from scipy.optimize import curve_fit

#--------------------------------
        # Les frames d'entrées
import LocalTkinter.Fichiers as Fichiers
#import Fichiers
from pydc1394 import Camera
# la camera est appellée par son uid
#pour l'avoir: 
#from pydc1394.camera2 import Context
#for c in Context().cameras:
#    print(c)
#(2892819673481529, 0) => F146B
#(2892819673575448, 0) => F201B

#from FakeCamera import Camera

class LeGUI(Frame):
    def __init__(self, master):
        self.master = master
        self.F146B=2892819673481529
        self.F201B=2892819673575448
        self.guidCam=self.F146B
        self.guidCam=self.F201B
        Frame.__init__(self, self.master)
        self.configure_gui()
        self.create_widgets()

    def configure_gui(self):
        self.erreur=StringVar();self.erreur.set("")
        # Parametre de la camera 
        self.tint=DoubleVar()
        #self.tint.trace("w",self.TintModifie) => def TintModifie(self,*args):
        self.gain=IntVar()
        self.Stop=False
        # ------ Initialisation de la camera
        #self.cam=Camera(guid=2892819673481529) 
        self.cam=Camera(guid=self.guidCam) 
        self.lemodel=self.cam.model.decode()[-5:]
        # acquisition en cours
        self.Acquisition=0
        # axe x: lambda ou pixel:
        self.EnMicron=BooleanVar();self.EnMicron.set(False)
        # fit gaussienne
        self.fitgauss=BooleanVar();self.fitgauss.set(False)
        self.w0=IntVar();self.w0.set(80)
        # borner
        self.borner=BooleanVar();self.borner.set(False)
        self.Pix0=IntVar();self.Pix0.set(0)
        self.Pix1=IntVar();self.Pix1.set(1234)
        #init graph
        self.InitGraph=BooleanVar()
        self.InitGraph.set(True)
        # focale pixel/micron
        self.focale=DoubleVar();self.focale.set(6.6)
        #  Nom de base du Fichier de sauvegarde
        self.Nom=StringVar()
        # le dossier de travail
        self.WorkDir=StringVar()
        self.WorkDir.set(os.getcwd())
        #fichier reference
        self.FichRef=StringVar();self.FichRef.set("!! Ldb non definie !!")

        
    def create_widgets(self):
        self.master.title("CPL Stingray "+self.lemodel)
        topframe=Frame(self.master)
        topframe.pack()
        nbook=ttk.Notebook(topframe)
        f1=ttk.Frame(nbook)
        f2=ttk.Frame(nbook)
        nbook.add(f1,text="Commandes")
        nbook.add(f2,text="Fichiers")
        nbook.pack()

        self.FrCommandes(f1).pack()
        Fichiers.TkFich(f2,self.Nom,self.FichRef, self.WorkDir)
        


        
        #Les  spectres dans une frame Toplevel: FrameTraceSp
        self.FrameTraceSp=Toplevel() # graphe a part
        self.FrameTraceSp.title("Image")
                   
        # de matplotlib.figure:
        self.Figspectre=Figure(figsize=(8,6),dpi=100) # figsize: H,V 
        self.plot1=self.Figspectre.add_subplot(111)
        # transfert la figure matplot dans un canvas Tk, inclus ds FrameTraceSp :
        self.canvas = FigureCanvasTkAgg(self.Figspectre,self.FrameTraceSp)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(self.canvas,self.FrameTraceSp)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
        #self.canvas.draw
    
    #------------------------------------------------------------------
    # mise a jour du graphe par 
    # FuncAnimation(my_gui.Figspectre,my_gui.animate,interval=1000) 
    # à la fin
    #------------------------------------------------------------------
    
    def func(self,x,mean,std,maxi):
    	return maxi*np.exp(-2*(x-mean)**2 / std**2) 
    
    def updatefig(self,i):
        if  self.Acquisition:
            #capture une frame et la copy dans CamArray
            self.cam.start_one_shot()
            frame =self.cam.dequeue()
            self.CamArray = frame.copy()
            frame.enqueue()
            self.cam.stop_one_shot()
            # on recupere les info de la camera
            y1=self.CamArray.sum(axis=1)/self.CamArray.shape[1]
            # reduction des bornes :
            if self.borner.get():
                y1=y1[self.Pix0.get():self.Pix1.get()]
            #4.4microns/pixel pour la F201B
            #4.65 pour la F146B
            #calibration avec la mire de calibration Leitz pour le "1.3"
            if  self.EnMicron.get():
                G=200./self.focale.get()
               # print("focale:{}, G={}".format(self.focale.get()*1.,G))
                x=np.arange(y1.size)*4.4/G 
                larg =int(2* self.w0.get()/4.4*G)
               # print("largeur en pixel:{}".format(larg))
            else : 
             #   self.focale.get()
                x=np.arange(y1.size)
                larg =int( self.w0.get())
            self.data=np.column_stack((x,y1))
            maxi= np.max(np.array(y1))
            
            if self.fitgauss.get():
                x_data = x[np.argmax(y1)-larg: np.argmax(y1)+larg]
                y_data = y1[np.argmax(y1)-larg: np.argmax(y1)+larg]
                init= [x[np.argmax(y1)],larg,maxi]
                b1= [0.7*x[np.argmax(y1)],0.5*larg,0.7*maxi]
                b2= [1.3*x[np.argmax(y1)],2*larg,1.3*maxi]
                try :
                    popt, pcov = curve_fit(self.func, x_data, y_data,\
                                           p0 = init)
                                          #bounds=(b1,b2))
                except RuntimeError :
                    print("fit pas bon!!!")
                    self.fitgauss.set(False)
            #    print(popt)
         
            #--------------------- affichage
            if self.initaffiche or self.InitGraph.get():
                self.plot1.clear()
                #self.l1,=self.plot1.plot(x,y1,label="ecart type :{}".format(ecart_type))
                self.l1,=self.plot1.plot(x,y1,label="cam")
                if self.fitgauss.get():
                    self.plot1.plot( x_data,self.func(x_data, *popt),\
    label="mean : {:.3f}, 2w(1/e2) : {:.3f}".format(popt[0], 2*popt[1]))
                self.plot1.set_ylabel("Intensite")
                self.plot1.legend(loc="upper left")

                if self.EnMicron.get():
                    self.plot1.set_xlabel("micron")
                else :
                    self.plot1.set_xlabel("pixel")
                self.initaffiche=False
            else :
                self.l1.set_data(x,y1)
            #self.canvas.draw()

            

#-------------------------------------------------
#Démarre le spectre:
#    * desactivation des boutons
# la variable self.Acquisition donne l'état de l'acquisition
#-------------------------------------------------
    def goSp(self,spectre):
#        os.chdir(self.WorkDir.get())
#        Nom=self.Nom.get()+str(len(glob.glob(self.Nom.get()+"*")))
#        self.FichSauve=Nom
        self.erreur.set('')
        self.goSpectre.configure(state=DISABLED)
        #tps d attente pour interroger le buffer en ms: 
        #self.delay=50 if self.cam.shutter.absolute<0.05 else  self.cam.shutter.absolute
        self.delay=50
        time.sleep(0.2)
        self.iter=0
        #print(self.delay)
        self.cam.start_capture()
        #self.cam.start_video()
        self.Acquisition=1
        self.initaffiche=True

    def StopImage(self):
        if self.Acquisition:
            self.Acquisition=0
            time.sleep(0.1)
            self.cam.stop_capture()
            print("Stop")
            self.goSpectre.configure(state=NORMAL)
        
    def Quitte(self):
        if self.Acquisition:
            self.Acquisition=0
            time.sleep(self.delay*2e-3)
        self.cam.close()
        self.master.destroy()
        


    
#--------------------------------------------------------------
        # une frame pour les commandes 
#--------------------------------------------------------------
    def FrCommandes(self,mere):
        frame=Frame(mere, bd=3,pady=2)
       # frame.pack()
        col=0
        ligne=0
        # ---------------- 4 boutons
        self.goSpectre=Button(frame, text="Démarre",command=lambda : self.goSp(1))
        self.goSpectre.grid(row=ligne,column=col)
        ttk.Button(frame, text="Stop",command= lambda: self.StopImage())\
                .grid(row=ligne,column=col+1)
        ttk.Button(frame, text="Enr.",command= self.EnregistreSP)\
                .grid(row=ligne,column=col+2)
        Button(frame, text="Close", command= lambda: self.Quitte())\
                .grid(row=ligne,column=col+4)

        ligne+=1;col=0
        ttk.Separator(frame,orient='horizontal').grid(row=ligne,columnspan=5,sticky='EW')
        #------------- options fit gausse et autoscale :        
        ligne+=1;col=0
        Checkbutton(frame,variable=self.fitgauss,text="Fit Waist")\
                .grid(row=ligne,column=col)
        Entry(frame,textvariable=self.w0,width=4).grid(row=ligne,column=col+1)
        Checkbutton(frame,variable=self.InitGraph,text="AutoSc.")\
                .grid(row=ligne,column=col+2)
        # --- pixel/microns
        ligne+=1;col=0
        ttk.Separator(frame,orient='horizontal').grid(row=ligne,columnspan=5,sticky='EW')
        ligne+=1;col=0
        Label(frame,text="f(mm)=").grid(row=ligne,column=col,sticky='E')
        Entry(frame,textvariable=self.focale,width=4).grid(row=ligne,column=col+1,sticky='W')
        Checkbutton(frame,variable=self.EnMicron,text="Pix/mic.")\
                .grid(row=ligne,column=col+2)


        #-------------- les bornes
        ligne+=1;col=0
        ttk.Separator(frame,orient='horizontal').grid(row=ligne,columnspan=5,sticky='EW')
        ligne+=1
        lesbornes=LabelFrame(frame,text="Bornes en Pixel",bd=3,pady=4)
        lesbornes.grid(row=ligne,column=col,columnspan=5,sticky='EW')
        Checkbutton(lesbornes,text="Borne",variable=self.borner).pack(side=LEFT) 
        Entry(lesbornes,textvariable=self.Pix0,width=4).pack(side=LEFT)
        Entry(lesbornes,textvariable=self.Pix1,width=4).pack(side=LEFT)

        #-------------------- erreurs/info
        ligne+=1;col=0
      #  Label(frame,textvariable=self.FichRef).grid(row=ligne,column=col,columnspan=5)
        Label(frame,textvariable=self.erreur).grid(row=ligne+1,column=col,columnspan=4)

        return frame
#--------------------------------------------------------------
    def EnregistreSP(self):
        os.chdir(self.WorkDir.get())
        Nom=self.Nom.get()+str(len(glob.glob(self.Nom.get()+"*")))
        Nom+=".sp"
        print("Fichier sauvé sur "+Nom+" dans "+self.WorkDir.get())
        if self.EnMicron.get():
            entete="Microns Intensite"
        else :
            entete="Pixel Intensite"
        np.savetxt(Nom,self.data,fmt="%g",header=entete)
        return 1

#--------------------------------------------------------------
if __name__ == '__main__':
    root = Tk()
    my_gui = LeGUI(root)
    ani=animation.FuncAnimation(my_gui.Figspectre,my_gui.updatefig,interval=50)
    root.mainloop()





