import socket, os, datetime, smtplib, fcntl, sys, os, time, tty, termios, subprocess
import matplotlib.pyplot as plt
import numpy as np
from subprocess import Popen, PIPE


#------ Capturar entrada teclado------------------
class raw(object):
    def __init__(self, stream):
        self.stream = stream
        self.fd = self.stream.fileno()
    def __enter__(self):
        self.original_stty = termios.tcgetattr(self.stream)
        tty.setcbreak(self.stream)
    def __exit__(self, type, value, traceback):
        termios.tcsetattr(self.stream, termios.TCSANOW, self.original_stty)

class nonblocking(object):
    def __init__(self, stream):
        self.stream = stream
        self.fd = self.stream.fileno()
    def __enter__(self):
        self.orig_fl = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl | os.O_NONBLOCK)
    def __exit__(self, *args):
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl)

print("Presione la tecla x para salir.")

#------------Clase-----------
class Sensor:
    def __init__(self):
        N=int(10**3); self.X=list(np.zeros(N)); self.Y=list(np.zeros(N)); self.Z=list(np.zeros(N)); self.A=list(np.zeros(N)); self.Angulo=list(np.zeros(N));
        self.dX=list(np.zeros(N)); self.dY=list(np.zeros(N)); self.dZ=list(np.zeros(N)); self.dA=list(np.zeros(N)); self.dAngulo=list(np.zeros(N))

    def getX(self): return(self.X)
    def getY(self): return(self.Y)
    def getZ(self): return(self.Z)
    def getA(self): return(self.A)
    def getAngulo(self): return(self.Angulo)
    def getdX(self): return(self.dX)
    def getdY(self): return(self.dY)
    def getdZ(self): return(self.dZ)
    def getdA(self): return(self.dA)
    def getdAngulo(self): return(self.dAngulo)
    def getName(self): return(str(__name__ ))

    def Actualizando(self,x1, y1, z1):
        x,y,z = float(x1), float(y1), float(z1)
        self.X.pop(0); self.Y.pop(0); self.Z.pop(0); self.A.pop(0); self.Angulo.pop(0) #elimina el primero
        self.dX.pop(0); self.dY.pop(0); self.dZ.pop(0); self.dA.pop(0); self.dAngulo.pop(0) #elimina el primero

        self.X.append(float(x)); self.Y.append(float(y)); self.Z.append(float(z))
        self.A.append((float(x)**2+float(y)**2+float(z)**2)**0.5)
        if y**2 + z**2+x**2!=0:  self.Angulo.append(np.arccos(z/(y**2 + z**2+x**2)**0.5) * 180/np.pi) #Angulo theta de esfericas en grados

        self.dX.append(self.X[-1]-self.X[-2]);  self.dY.append(self.Y[-1]-self.Y[-2])
        self.dZ.append(self.Z[-1]-self.Z[-2]);  self.dA.append(self.A[-1]-self.A[-2])
        self.dAngulo.append(self.Angulo[-1]-self.Angulo[-2])

    def Imagen(self, t, angulo = False):
        if t==1: plt.legend(loc='upper left');

        if angulo==True:
            plt.ylim([0,np.pi]); plt.xlabel("t"); plt.ylabel(self.getName())
            plt.scatter(t,float(self.getAngulo()[-1]), label= "dAngulo")
        else:
            plt.ylim([-100,100]); plt.xlabel("t"); plt.ylabel(self.getName())
            plt.scatter(t,float(self.getdX()[-1]), s=5,c='b', label='dX')
            plt.scatter(t,float(self.getdY()[-1]), s=5,c='g', label='dY')
            plt.scatter(t,float(self.getdZ()[-1]), s=5, c='y', label='dZ')
            plt.scatter(t,float(self.getdA()[-1]), s=20, c='r', label='dA' )
        plt.pause(0.001);

#-----------Creando email-----------
def Email(sent_body):
    gmail_user = 'iaun2019pe@gmail.com'
    gmail_password = 'Qwert54321'

    sent_from = gmail_user
    sent_to = ['ddfulaa@unal.edu.co', 'mstorresh@unal.edu.co','gjalvarezc@unal.edu.co', 'saguileran@unal.edu.co']
    sent_subject = 'OMG Super Important Message'
   # body = 'Ohhhh my joint has fallen'

    email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(sent_to), sent_subject, sent_body)
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, sent_to, email_text)
    server.close()
    print ('Email sent!')

#-------------Creando conexion-------------------

UDP_IP_ADDRESS = "192.168.1.13"
UDP_PORT_NO = 5555

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#serverSock.close()
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

#--------------Tomando Datos---------------------------
flag, caida, caida1, caida2= False, False, False, False
GPS = Sensor(); Acelerometro = Sensor(); Giroscopio = Sensor()
Gravedad = Sensor();#83
Aceleracion_lineal= Sensor() #82
t, i = 0, 0
tolacel, tolgrav, tolang = 16, 10, 4
plt.xlabel("t"); plt.ylabel("Value")

with raw(sys.stdin):
    with nonblocking(sys.stdin):
        while True:
            try:
                keypressed = sys.stdin.read(1)
                data, addr = serverSock.recvfrom(1024)
                Data = data.decode("utf-8").split(",")

                if Data.count(' 1')>0:  GPS.Actualizando(float(Data[Data.index(' 1')+1]), float(Data[Data.index(' 1')+2]), float(Data[Data.index(' 1')+3]))
                if Data.count(' 3')>0:  Acelerometro.Actualizando(float(Data[Data.index(' 3')+1]), float(Data[Data.index(' 3')+2]), float(Data[Data.index(' 3')+3]))
                if Data.count(' 4')>0:  Giroscopio.Actualizando(float(Data[Data.index(' 4')+1]), float(Data[Data.index(' 4')+2]), float(Data[Data.index(' 4')+3] ))

                Acelerometro.Imagen(t, False); t+=1
                #-------------Primer Detector-----------
                #--- Pruebas con el acelerometro lineal y la gravedad
                if Data.count(' 83')>0 and Data.count(' 82')>0:
                    grav = np.array([float(Data[Data.index(' 83')+1]),float(Data[Data.index(' 83')+2]),float(Data[Data.index(' 83')+3])])
                    acclin = np.array([float(Data[Data.index(' 82')+1]),float(Data[Data.index(' 82')+2]),float(Data[Data.index(' 82')+3])])
                    Gravedad.Actualizando(float(Data[Data.index(' 83')+1]),float(Data[Data.index(' 83')+2]),float(Data[Data.index(' 83')+3]))
                    Aceleracion_lineal.Actualizando(float(Data[Data.index(' 82')+1]),float(Data[Data.index(' 82')+2]),float(Data[Data.index(' 82')+3]))

                    #plt.scatter(t,float(np.linalg.norm(acclin)))
                    #plt.pause(0.001);                    t+=1
                    if np.linalg.norm(acclin) > tolgrav: #Prueba con gravity y vector aceleracion
                        coseno = np.dot(grav,acclin)/(np.linalg.norm(grav)*np.linalg.norm(acclin))
                        if coseno < -0.90:  caida = True
                            #print("Caida! Coseno: "+ str(coseno)+ " norma: "+ str(np.linalg.norm(acclin)))
                #----Segundo Detector (ACELEROMETRO)------
                #print(Acelerometro.getdA()[-1])
                if Acelerometro.getdA().count(0)<999 and abs(Acelerometro.getdA()[-1]) > tolacel:   caida1 = True; 
                #----Tercer Detector------
                #if abs(Acelerometro.getdAngulo()[-1]) > tolang:        #    caida2 = True
                #--------Confirmacion de caida------------
                if Giroscopio.getX().count(0)>999:
                    if (caida or caida1) and (not flag):
                        print("Atention, a fall has occured!")
                        #Email("Your grandparent has fallen at latitude {}, longitude {} and height  = {} the day {} at {} time. To locate this position go to https://www.gps-coordinates.net and enter the latitude and longitude.".format(GPS.getX()[-1], GPS.getY()[-1], GPS.getZ()[-1], str(datetime.datetime.now().date()) , str(datetime.datetime.now().time())[:8]))
                        flag = True #Para no enviar mas correos
                else:
                    if (caida and caida1) and (not flag):
                        print("Atention, a fall has occured!")
                        #Email("Your grandparent has fallen at latitude {}, longitude {} and height  = {} the day {} at {} time. To locate this position go to https://www.gps-coordinates.net and enter the latitude and longitude.".format(GPS.getX()[-1], GPS.getY()[-1], GPS.getZ()[-1], str(datetime.datetime.now().date()) , str(datetime.datetime.now().time())[:8]))
                        flag = True #Para no enviar mas correos
                #print(repr(keypressed))
                
                if keypressed=="x":
                    break
            except IOError:
                print('Not ready')

#------------------Creating txt----------------
file = open("./Data/"+str(datetime.datetime.now().date())+" - "+str(datetime.datetime.now().time())[:8]+".txt", 'w')
file.write(" {} W {} W {} \n".format(Acelerometro.getX(), Acelerometro.getY(), Acelerometro.getZ()))
file.write(" {} W {} W {} \n".format(Giroscopio.getX(), Giroscopio.getY() ,Giroscopio.getZ()))
file.write(" {} W {} W {} \n".format(Gravedad.getX(), Gravedad.getY(), Gravedad.getZ()))
file.write(" {} W {} W {} \n".format(Aceleracion_lineal.getX(), Aceleracion_lineal.getY(), Aceleracion_lineal.getZ()))
comment = input("Insert comment: ")
file.write(comment)
file.close()
#-----------------Uploading to git----------------
#os.system("git remote set-url origin https://name:password@github.com/repo.git")
os.system("sudo git pull")
os.system("sudo git add --all")
os.system("sudo git commit -m "+str(datetime.datetime.now().date())+"-"+str(datetime.datetime.now().time())[:8])
os.system("sudo git push")

plt.show()
plt.savefig("./Pictures/"+str(datetime.datetime.now().date())+"-"+str(datetime.datetime.now().time())[:8]+".png")
plt.pause(0.001)
plt.close()
