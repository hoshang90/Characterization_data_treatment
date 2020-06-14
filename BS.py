#!/usr/bin/python3
import serial
import time 

class BabSoleil:
    """ Classe qui permet de piloter un BS via
    le RS232. 
    Attention: pas de controle sur la mise en marche de la commande
    le programme attend indéfiniment la réponse du ESP30x
    Usage:
        from BS import BabSoleil;
        leBS=BAbSoleil(moteur="1", leport="/dev/ttyUSB0",bdr=19200)
        par default: /dev/ttyPS3
        leBS #affiche les info et lit la phase (bs.LitPosdeg())
        help(leBS)

        leBS.Vamm(320) # va a la position en mm
        leBS.VaLbda(0.5) # va a la position en frac de lambda
        leBS.LitPos() #retourne la valeur et affecte leBS.pos
        leBS.LitLbda() #retourne la valeur en frac de lambda

    Créé le 25 Octobre 2019 par  Guy sur debian testing et l'ESP301

    """
    def __init__(self,moteur="1", leport="/dev/ttyPS3",bdr=19200,
            ZeroLbda=24.7617,UnLbda=6.517):
        self.ESP300=serial.Serial(port=leport,baudrate=bdr) 
        self.ESP300.open
        self.ZeroLbda=ZeroLbda
        self.UnLbda=UnLbda
        if self.ESP300.isOpen:
            print ("-"*20)
            print("Commande: "+self.ESP300.name+' is open ..')
        #on flush
       # print ("Pensez au homing sur le moteur {0}".format(moteur))
        self.ESP300.flushInput
        self.ESP300.flushOutput
        self.moteur=moteur
       # print (" Position actuelle ...")
        self.LitPos()
       # print("{0}  mm".format(self.pos))
                #moteur ON
        commande=self.moteur+"MO\r"
        self.ESP300.write(commande.encode('ascii'))
        #controle de la vitesse :ok en Fevrier 2017
        
#        print("*Se positionner à la valeur en mm")
#        print(" =>a.Vamm(valeur) //reprend la main quand le moteur stop")
#        print("*Se positionner à la valeur en frac de lambda")
#        print(" =>a.VaLbda(valeur) //reprend la main quand le moteur stop")
#        print(" =>a.Bouge(valeur) //reprend la main de suite")
#        print("*Lecture: a.LitPos() ")
#        print ("-"*20)

    def __repr__(self):
        """ Affichage cool """
        reponse="-"*20+"\n"
        reponse+="Port RS232: (leBS.ESP300.name) "+self.ESP300.name+"\n"
        reponse+="N° moteur: (leBS.moteur) "+ self.moteur+"\n"
        reponse+="Vitesse: {}".format(self.LitVitesse())
        reponse+="\nPosition actuelle ... (bs.LitPos() )\n" 
        self.LitPos()
        reponse+="leBS.pos= {0} mm \n".format(self.pos)
        reponse+="0lambda (leBS.ZeroLbda): {}\n".format(self.ZeroLbda)
        reponse+="1lambda (leBS.UnLbda): {}\n".format(self.UnLbda)
        reponse+="-"*20+"\n"
        return reponse


   

    def Vamm(self,position):
        """ Va à la position en mm, attend que le
        moteur s arrete, affecte et retourne la position"""
        # string avec une precision à 2 chiffres apres la virgule
        x="%.3f" % position
        commande=self.moteur+"PA"+x+"\r"
        self.ESP300.write(commande.encode('ascii'))
        # on attend que le moteur s arrete
        while self.MoteurBouge():
            time.sleep(0.2) #secondes
        self.pos=self.LitPos()
        return self.pos

    def VaLbda(self,philambda):
        """ Va à la position en fraction de lambda attend que le
        moteur s arrete, affecte et retourne la position """
        PosEn_mm=(philambda-1)*(self.UnLbda-self.ZeroLbda)+self.UnLbda
        x=self.Vamm(PosEn_mm)
        Pos_En_lbda=(x-self.UnLbda)/(self.UnLbda-self.ZeroLbda)+1
        return(Pos_En_lbda)

    def LitLbda(self):
        """ position en fraction de lambda """
        x=self.LitPos()
        Pos_En_lbda=(x-self.UnLbda)/(self.UnLbda-self.ZeroLbda)+1
        return(Pos_En_lbda)


    def Bouge(self,position):
        """ Va à la position """
        # string avec une precision à 2 chiffres apres la virgule
        x="%.2f" % position
        commande=self.moteur+"PA"+x+"\r"
        self.ESP300.write(commande.encode('ascii'))
        return 1

    def MoteurBouge(self):
        """ interroge l'ESP300 pour savoir si un moteur est en mouvement """
        self.ESP300.write(b'TS\r')
        bits=self.ESP300.readline() #des bytes finissant par "\r\n"
        reponse=bits.rstrip(b'\r\n').decode()
        return reponse != "P"



    def LitPos(self):
        """ position en mm  """
        #on demande la valeur
        commande=self.moteur+"TP\r"
        self.ESP300.write(commande.encode('ascii'))
        #on la lit
        rep=self.ESP300.readline()
        #c est un binaire b'5.00\r\n'
        self.pos=float(rep.rstrip(b'\r\n').decode())

        # rstrip() enleve la fin et  decode convertit en ascii
        # puis float convertit d ascii en float
                    #on peut aussi  convertir en string avec str(rep,'utf-8')
        return self.pos

    def LitVitesse(self):
        """ vitesse en mm/° """
        #on demande la valeur
        commande=self.moteur+"VA?\r"
        self.ESP300.write(commande.encode('ascii'))
        #on la lit
        rep=self.ESP300.readline()
        #c est un binaire b'5.00\r\n'
        vitesse=float(rep.rstrip(b'\r\n').decode())

        # rstrip() enleve la fin et  decode convertit en ascii
        # puis float convertit d ascii en float
                    #on peut aussi  convertir en string avec str(rep,'utf-8')
        return vitesse



