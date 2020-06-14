#!/usr/bin/python3
# -*-coding:Utf-8 -*
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
import os, glob
import numpy as np
import matplotlib.pyplot as plt
import ClassAcquisitionStokesCamera;cp=ClassAcquisitionStokesCamera.CameraPolar()
import ClassTraitStokesCamera;st=ClassTraitStokesCamera.Stokes()

class Stocks_GUI(Frame):
    def __init__(self, master):
        self.master = master
        Frame.__init__(self, self.master)
        self.configure_gui()
        self.create_widgets()
#--------------------------------------------------------------
        ######### Acquisition ############# 
#--------------------------------------------------------------
        self.name_entry.bind("<Return>", (lambda event: self.By_enter(self.Save_as_en, self.Npy_file_save)))#updating by enetry in the entry
        self.name_entry.bind("<<ComboboxSelected>>", (lambda event: self.By_enter(self.Save_as_en,self.Npy_file_save)))#updating by selecting one of the list
        self.defaultBackground = self["background"] 
        self.bb_goto_bot.bind("<Enter>",lambda event:self.by_mouse(self.bb_goto_bot))
        self.bb_goto_bot.bind("<Leave>",lambda event:self.by_mouse_leave(self.bb_goto_bot))
        self.lam_makezero_bot.bind("<Enter>",lambda event:self.by_mouse(self.lam_makezero_bot))
        self.lam_makezero_bot.bind("<Leave>",lambda event:self.by_mouse_leave(self.lam_makezero_bot))
        self.lam_goto_bot.bind("<Enter>",lambda event:self.by_mouse(self.lam_goto_bot))
        self.lam_goto_bot.bind("<Leave>",lambda event:self.by_mouse_leave(self.lam_goto_bot))
        self.measure_bot.bind("<Enter>",lambda event:self.by_mouse(self.measure_bot))
        self.measure_bot.bind("<Leave>",lambda event:self.by_mouse_leave(self.measure_bot))
        self.save_as_bot.bind("<Enter>",lambda event:self.by_mouse(self.save_as_bot))
        self.save_as_bot.bind("<Leave>",lambda event:self.by_mouse_leave(self.save_as_bot))
        self.exit_bot.bind("<Enter>",lambda event:self.by_mouse(self.exit_bot))
        self.exit_bot.bind("<Leave>",lambda event:self.by_mouse_leave(self.exit_bot))
#--------------------------------------------------------------
        ######### Treatment ############# 
#--------------------------------------------------------------
        self.Browsfile_entry.bind("<Return>", (lambda event: self.By_enter(self.Browsfile_en, self.Browsfile_str)))#updating by enetry in the entry
        self.Browsfile_entry.bind("<<ComboboxSelected>>", (lambda event: self.By_enter(self.Browsfile_en, self.Browsfile_str)))#updating by selecting one of the list
        self.exit2_bot.bind("<Enter>",lambda event:self.by_mouse(self.exit2_bot))
        self.exit2_bot.bind("<Leave>",lambda event:self.by_mouse_leave(self.exit2_bot))
    def configure_gui(self):
#--------------------------------------------------------------
        ######### Acquisition ############# 
#--------------------------------------------------------------
        self.Lamon4=DoubleVar();self.Lamon4.set(0)
        self.Measure_step=IntVar();self.Measure_step.set(10)
        self.Nstep=IntVar();self.Nstep.set(int(360/self.Measure_step.get()+1))
        self.Bb_lam=DoubleVar();self.Bb_lam.set(0)
        self.Activate_steps=BooleanVar();self.Activate_steps.set(False)
        self.Npy_file_save=StringVar();self.Npy_file_save.set("lambda0")
        self.Save_As_var=StringVar();self.Save_As_var.set((os.getcwd()+"/"+self.Npy_file_save.get()).replace(os.sep, '/'))############
#--------------------------------------------------------------
        ######### Treatment ############# 
#--------------------------------------------------------------
        self.checkbutton1_var=BooleanVar();self.checkbutton1_var.set(False)
        self.checkbutton2_var=BooleanVar();self.checkbutton2_var.set(False)
        self.checkbutton3_var=BooleanVar();self.checkbutton3_var.set(False)
        self.checkbutton4_var=BooleanVar();self.checkbutton4_var.set(False)
        self.checkbutton5_var=BooleanVar();self.checkbutton5_var.set(False)
        self.Browsfile_str=StringVar();self.Browsfile_str.set("lambda0.npy")
        self.Browsfile_str_var=StringVar()
        self.Browsfile_str_var.set((os.getcwd()+"/"+self.Browsfile_str.get()).replace(os.sep, '/'))############
        self.Default_function=StringVar();self.Default_function.set("Moy_choose")
        self.Frame_numb_var=IntVar();self.Frame_numb_var.set(12)

    def create_widgets(self):
        self.master.title("Stocks parameters measurement")
        topframe=Frame(self.master)
        topframe.pack()
        nbook=ttk.Notebook(topframe)
        f1=ttk.Frame(nbook)
        f2=ttk.Frame(nbook)
        nbook.add(f1,text="Acquisition")
        nbook.add(f2,text="Treatment")
        nbook.pack()
#--------------------------------------------------------------
        ######### Acquisition ############# 
#--------------------------------------------------------------
        self.Acquisition_part(f1).pack()
#--------------------------------------------------------------
        ######### Treatment ############# 
#--------------------------------------------------------------
        self.Treatment_part(f2).pack()
#--------------------------------------------------------------
        ######### Acquisition ############# 
#--------------------------------------------------------------        
    def Acquisition_part(self,mere):
        frame=Frame(mere, bd=13,pady=2)
        col=0;ligne=0
        ttk.Label(frame, text="Quarter waveplate",font = 'Times 12').grid(row=ligne, column=col,columnspan=2)
        col=0;ligne+=1
        # ---------------- 4 boutons
        self.lam_goto_bot=Button(frame,text="Go to angle",command=lambda:self.Lam4_goto_fun(), width=10)#, relief=RAISED)
        self.lam_goto_bot.grid(row=ligne,column=col,padx=5, pady=5)
        self.lam_makezero_bot=Button(frame, text="Make Zero",relief=RAISED, command=lambda:self.Lam4_makezero_fun(), width=10)
        self.lam_makezero_bot.grid(row=ligne,column=col+1,padx=5,pady=5)
        ligne+=1;col=0
        ttk.Combobox(frame, width=10, textvariable=self.Lamon4, values=list(np.arange(0,390,30, dtype=int))).grid(row=ligne, column=col, padx=5, pady=5)
        ttk.Separator(frame,orient='horizontal').grid(row=ligne+1,columnspan=10,sticky='EW')
        ligne+=3
        ttk.Label(frame,text="").grid(row=ligne-2,column=col,pady=5)
        #second part
        col=3;ligne=0
        ttk.Separator(frame,orient=VERTICAL).grid(row =ligne, column=col+1,rowspan=3,sticky='ns', padx=5)
        ttk.Label(frame, text="Babinet–Soleil",font = 'Times 12').grid(row=ligne, column=col+2,columnspan=2)
        self.bb_goto_bot=Button(frame,text="Go to Lbda",command=lambda:self.bs_goto_fun(), width=10, relief=RAISED)
        self.bb_goto_bot.grid(row=ligne+1,column=col+2,padx=5,pady=5)
        ttk.Combobox(frame, width=10, textvariable=self.Bb_lam,values=list(np.arange(0,1,0.125, dtype=float))).grid(row=ligne+2, column=col+2, padx=5, pady=5)
        self.exit_bot=Button(frame, text="Close",width=10, command= lambda: self.close_all())
        self.exit_bot.grid(row=ligne+8,column=col+3, padx=5,pady=5)
        #third part
        ligne=5;col=0
        self.MeasureParam=LabelFrame(frame,text="Measurement parameters",bd=3,pady=4)
        self.MeasureParam.grid(row=ligne,column=col,columnspan=2,sticky='EW')
        Checkbutton(self.MeasureParam,text="Steps",command=self.naccheck,variable=self.Activate_steps).pack(side=LEFT) 
        self.Activate_by_check=Entry(self.MeasureParam,textvariable=self.Measure_step,width=8)
        self.Activate_by_check.pack(side=LEFT,padx=5);self.Activate_by_check.configure(state=DISABLED)
        self.measure_bot=Button(frame, text="Measure",relief=RAISED, command=lambda:self.Aq_measure_fun(),width=10)
        self.measure_bot.grid(row=ligne+2,column=col+2, padx=5, pady=5)
        ligne+=2;col=0
        self.labelFrame = LabelFrame(frame, text="Save the file as");self.labelFrame\
                .grid(row=ligne,column=col,columnspan=2,sticky='EW')
        self.labelFrame1 = LabelFrame(frame, text="Save as");self.labelFrame1\
                .grid(row=ligne,column=col+3,columnspan=2,sticky='EW')
        self.name_entry=ttk.Combobox(self.labelFrame,textvariable=self.Npy_file_save,width=12,\
                values= ["lambda0","lambda0p125","lambda0p25","lambda0p375","lambda0p5","lambda0p625","lambda0p75","lambda0p875"]);self.name_entry.pack();
        self.Save_as_en=Label(self.labelFrame, text=self.Save_As_var.get());self.Save_as_en.pack()
        self.save_as_bot=Button(self.labelFrame, text="Save As", command=lambda:self.file_save_as());self.save_as_bot.pack()
        return frame
    def file_save_as(self):
        """Ask the user where to save the file and save it there. 
        Returns True if the file was saved, and False if the user
        cancelled the dialog.
        """
        self.save_as_path =filedialog.asksaveasfilename(initialdir=os.getcwd(),initialfile=self.Npy_file_save.get()\
                , title="Select As")#,filetypes=("json", "*.json")
        if self.save_as_path:
            #print(self.save_as_path)
            self.Save_as_en.configure(text=self.save_as_path)
            self.Save_As_var.set(self.save_as_path)
        else:
            tk.messagebox.showinfo("Warning",'Please try again to save the file')
    def by_mouse(self,current_button):
        current_button.configure(bg='green',fg="white")
    def by_mouse_leave(self,current_button):
        current_button.configure(bg=self.defaultBackground,fg="black") 
    def By_enter(self,current_label, var):
        """Ask the user where to save the file and save it there. 
        Returns True if the file was saved, and False if the user
        cancelled the dialog.
        """
        current_label.configure(text=(os.getcwd()+"/"+var.get()).replace(os.sep, '/'))

    def naccheck(self):#modify when check boutton is chosen
        if self.Activate_steps.get() == False:
            self.Activate_by_check.configure(state='disabled')
        else:
            self.Activate_by_check.configure(state='normal')
    def Lam4_goto_fun(self):
        cp.l4.VaPos(self.Lamon4.get())
    def Lam4_makezero_fun(self):
        cp.l4.Zero()
    def bs_goto_fun(self):
        cp.bs.VaLbda(self.Bb_lam.get())
    def Aq_measure_fun(self):
        #print("cp.Mesure(attente=1,fich={},Npas={},pas={})".format(self.Save_As_var.get(),int(360/self.Measure_step.get()+1),self.Measure_step.get()))
        cp.Mesure(attente=1,fich=self.Save_As_var.get(),Npas=int(360/self.Measure_step.get()+1),pas=self.Measure_step.get())
#
#--------------------------------------------------------------
        ######### Treatment ############# 
#--------------------------------------------------------------
    def Treatment_part(self,mere):
        frame=Frame(mere, bd=13,pady=2)
        col=0;ligne=0
        ttk.Label(frame, text="Choose a function",font = 'Times 12').grid(row=ligne, column=col,columnspan=1)
        col=0;ligne+=1
        # ---------------- 4 boutons
        ligne+=1;col=0
        self.Treat_combobox=ttk.Combobox(frame, width=18, textvariable=self.Default_function, values=["Moy_choose","Save_stocks_choose","Carto_choose","S3_from_stocks"])
        self.Treat_combobox.grid(row=ligne, column=col, padx=5, pady=5)
        self.run_bot=Button(frame,text="Run",command=lambda:self.run_function(), width=10, relief=RAISED)
        self.run_bot.grid(row=ligne,column=col+1,padx=5,pady=5)
        ttk.Separator(frame,orient='horizontal').grid(row=ligne+2,columnspan=10,sticky='EW')
        self.Frame_numb_label=Label(frame, text="Frame #");self.Frame_numb_label.place(x=0,y=65) 
        self.Frame_num_entry=Entry(frame,textvariable=self.Frame_numb_var,width=8)
        self.Frame_num_entry.grid(row=ligne+1, column=col, padx=5, pady=5) 
        col+=1
        self.checkbutton1=Checkbutton(frame,text="show image",variable=self.checkbutton1_var)
        self.checkbutton1.grid(row=ligne+1, column=col, padx=5, pady=5)
        self.checkbutton2=Checkbutton(frame,text="Animate",variable=self.checkbutton2_var)
        self.checkbutton2.grid(row=ligne+1, column=col+1, padx=5, pady=5)
        self.checkbutton3=Checkbutton(frame,text="Save gif",variable=self.checkbutton3_var)
        self.checkbutton3.grid(row=ligne+1, column=col+2, padx=5, pady=5)
        self.checkbutton4=Checkbutton(frame,text="Save colored gif",variable=self.checkbutton4_var)
        self.checkbutton4.grid(row=ligne+1, column=col+3, padx=5, pady=5)
        col=0
        self.Browsfile_Lframe= LabelFrame(frame, text="Browse A File");self.Browsfile_Lframe\
                .grid(row=ligne+3,column=col,columnspan=2,sticky='EW')
        #self.checkbutton5=Checkbutton(self.Browsfile_Lframe,text="choose another file",command=self.naccheck,variable=self.checkbutton5_var)
        #self.checkbutton5.pack()
        self.Browsfile_entry=ttk.Combobox(self.Browsfile_Lframe,textvariable=self.Browsfile_str,width=12,\
                values= ["lambda0.npy","lambda0p125.npy","lambda0p25.npy","lambda0p375.npy",\
                "lambda0p5.npy","lambda0p625.npy","lambda0p75.npy","lambda0p875.npy"]);self.Browsfile_entry.pack();
        self.Browsfile_en=Label(self.Browsfile_Lframe, text=self.Browsfile_str_var.get());self.Browsfile_en.pack()
        self.Browsfile_bot=Button(self.Browsfile_Lframe, text="Browse A File", command=lambda:self.file_open());self.Browsfile_bot.pack()
        self.exit2_bot=Button(frame, text="Close",width=10, command= lambda: self.close_all())
        self.exit2_bot.grid(row=ligne+8,column=col+3, padx=5,pady=5)
        self.exit3_bot=Button(frame, text="Close Plots",width=10, command= lambda: self.close_plots())
        self.exit3_bot.grid(row=ligne+8,column=col+2, padx=5,pady=5)
        return frame

    def file_open(self): # to brows the file
        self.file_open_path = filedialog.askopenfilename(initialdir=os.getcwd(),\
                title="Select A File")#, filetype=(("Numpy files", "*.npy"),("all files", "*.*")))
        if self.file_open_path:
            self.Browsfile_en.configure(text=self.file_open_path)
            print(self.file_open_path)
            self.Browsfile_str_var.set(self.file_open_path)
        else:
            tk.messagebox.showinfo("Warning","You didn't pick any file")
        #print(self.filename)
    def run_function(self):
        if self.Default_function.get()=="Moy_choose":
           # print("frame num ",self.Frame_numb_var.get())
           # print("hello ",self.Default_function.get())
           # print("show image ",self.checkbutton1_var.get())
           # print("Animate ",self.checkbutton2_var.get())
           # print("Save gif ",self.checkbutton3_var.get())
           # print("Save colored gif ",self.checkbutton4_var.get())
            st.Moy_choose(fich=self.Browsfile_str_var.get(),frame_numb=self.Frame_numb_var.get(),show_image=self.\
                    checkbutton1_var.get(),anime=self.checkbutton2_var.get(),save_gif=self.checkbutton3_var.get(),\
                    save_colored_gif=self.checkbutton4_var.get())
        elif self.Default_function.get()=="Save_stocks_choose":
            #print("hello "+self.Default_function.get())
            st.Save_stocks_choose(fich=self.Browsfile_str_var.get(),frame_numb=self.Frame_numb_var.get(),show_image=self.\
                    checkbutton1_var.get(),anime=self.checkbutton2_var.get(),save_gif=self.checkbutton3_var.get(),\
                    save_colored_gif=self.checkbutton4_var.get())
        elif self.Default_function.get()=="Carto_choose":
            #print("hello "+self.Default_function.get())
            st.Carto_choose(bdf=70,fich=self.Browsfile_str_var.get(),frame_numb=self.Frame_numb_var.get(),show_image=self.\
                    checkbutton1_var.get(),anime=self.checkbutton2_var.get(),save_gif=self.checkbutton3_var.get(),\
                    save_colored_gif=self.checkbutton4_var.get())
        elif self.Default_function.get()=="S3_from_stocks":
            #print("hello "+self.Default_function.get())
            st.S3_from_stocks()#fich=self.Browsfile_str_var.get())
    def close_plots(self):
        plt.close('all')
    def close_all(self):
        self.master.destroy()
        plt.close('all')
#--------------------------------------------------------------
if __name__ == '__main__':
    root = Tk()
    the_gui = Stocks_GUI(root)
    #ani=animation.FuncAnimation(my_gui.Figspectre,my_gui.updatefig,interval=50)
    root.mainloop()





