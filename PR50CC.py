#!/usr/bin/python3
import serial
import time 

class rotation:
    """ Classe qui permet de piloter la lame L4 via
    le RS232. 
    Attention: pas de controle sur la mise en marche de la commande
    le programme attend indéfiniment la réponse du ESP30x
    Usage:
        from PR50CC import rotation;
        l4=rotation(moteur="2", leport="/dev/ttyUSB7",bdr=19200)
        polar=rotation(moteur="1", leport="/dev/ttyUSB7",bdr=19200)

        l4 #affiche les info et lit la phase (bs.LitPosdeg())
        help(l4)

        l4.VaPos(320) # va a la position en degre 
        l4.LitPos() #retourne la valeur et affecte l4.pos

    Créé le 25 Janvier 2017 par S. Guy sur debian testing et l'ESP301
        => A faire: 1Lambda en fonction de la longueur d'onde. (ChgeLbda) 

    """
    def __init__(self,moteur="2", leport="/dev/ttyPS3",bdr=19200,zdeg=90.0):
        self.ESP300=serial.Serial(port=leport,baudrate=bdr) 
        self.zdeg=zdeg
        self.ESP300.open
        if self.ESP300.isOpen:
        #    print ("-"*20)
            print("Lame:"+self.ESP300.name+' is open ..')
        #on flush
        self.ESP300.flushInput
        self.ESP300.flushOutput
        self.moteur=moteur
     #   print (" Position actuelle ...")
        self.LitPos()
      #  print("{0}  deg".format(self.pos))
                #moteur ON
        commande=self.moteur+"MO\r"
        self.ESP300.write(commande.encode('ascii'))
        #self.Home()
        #self.VaPos(self.zdeg)
        #self.Zero()
        #controle de la vitesse :ok en Fevrier 2017
        
#        print("*Se positionner à la valeur")
#        print(" =>a.VaPos(valeur) //reprend la main quand le moteur stop")
#        print(" =>a.Bouge(valeur) //reprend la main de suite")
#        print("*Lecture: a.LitPos() ")
#        print("Axe rapide horizontale pour {}".format(self.zdeg))
#        print("l4.VaPos({}) puis l4.Zero()".format(self.zdeg))
#        print ("-"*20)

    def __repr__(self):
        """ Affichage cool """
        reponse="-"*20+"\n"
        reponse+="Port RS232: (l4.ESP300.name)"+self.ESP300.name+"\n"
        reponse+="N° moteur: (l4.moteur)"+ self.moteur+"\n"
        reponse+="Vitesse: {}".format(self.LitVitesse())
        reponse+="Position actuelle ... (l4.LitPos() )\n" 
        self.LitPos()
        reponse+="l4.pos= {0} deg \n".format(self.pos)
        reponse+="-"*20+"\n"
        return reponse


   

    def VaPos(self,position):
        """ Va à la position en degre, attend que le
        moteur s arrete, affecte et retourne la position"""
        # string avec une precision à 2 chiffres apres la virgule
        x="%.2f" % position
        commande=self.moteur+"PA"+x+"\r"
        self.ESP300.write(commande.encode('ascii'))
        # on attend que le moteur s arrete
        while self.MoteurBouge():
            time.sleep(0.2) #secondes
        self.pos=self.LitPos()
        return self.pos

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
        """ position  """
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

    def Zero(self):
        """ met la valeur actuelle à zero """
        commande=self.moteur+"DH0\r"
        self.ESP300.write(commande.encode('ascii'))
        return 1

    def Home(self):
        """ met la valeur actuelle à zero """
        commande=self.moteur+"OR0\r"
        self.ESP300.write(commande.encode('ascii'))
        while self.MoteurBouge():
            time.sleep(0.2) #secondes
        return 1


