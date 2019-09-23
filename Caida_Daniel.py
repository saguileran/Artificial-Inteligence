import socket, os, datetime, smtplib, fcntl, sys, os, time, tty, termios
import matplotlib.pyplot as plt
import numpy as np

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
        self.X=list(np.zeros(10)); self.Y=list(np.zeros(10)); self.Z=list(np.zeros(10)); self.A=list(np.zeros(10)); self.Angulo=list(np.zeros(10));
        self.dX=list(np.zeros(10)); self.dY=list(np.zeros(10)); self.dZ=list(np.zeros(10)); self.dA=list(np.zeros(10)); self.dAngulo=list(np.zeros(10))

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

    def Actualizando(self,x1, y1, z1):
        x,y,z = float(x1), float(y1), float(z1)
        self.X.pop(0); self.Y.pop(0); self.Z.pop(0); self.A.pop(0); self.Angulo.pop(0) #elimina el primero
        self.dX.pop(0); self.dY.pop(0); self.dZ.pop(0); self.dA.pop(0); self.dAngulo.pop(0) #elimina el primero

        self.X.append(float(x)); self.Y.append(float(y)); self.Z.append(float(z))
        self.A.append((float(x)**2+float(y)**2+float(z)**2)**0.5)
        self.Angulo.append(np.arccos(z/(y**2 + z**2+x**2)**0.5) * 180/np.pi) #Angulo theta de esfericas en grados

        self.dX.append(self.X[-1]-self.X[-2]);  self.dY.append(self.Y[-1]-self.Y[-2])
        self.dZ.append(self.Z[-1]-self.Z[-2]);  self.dA.append(self.A[-1]-self.A[-2])
        self.dAngulo.append(self.Angulo[-1]-self.Angulo[-2])

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
UDP_IP_ADDRESS = "192.168.1.14"
UDP_PORT_NO = 5551

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#serverSock.close()
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

#--------------Tomando Datos---------------------------
flag, caida= False, False
GPS = Sensor(); Acelerometro = Sensor(); Girsocopio = Sensor()
Gravedad = Sensor() #83
Aceleracion_lineal= Sensor() #82
t=0
tolacel, tolgrav = 3, 8

with raw(sys.stdin):
    with nonblocking(sys.stdin):
        while True:
            try:
                keypressed = sys.stdin.read(1)
                data, addr = serverSock.recvfrom(1024)
                Data = data.decode("utf-8").split(",")

                if Data.count(' 1')>0:  GPS.Actualizando(Data[Data.index(' 1')+1], Data[Data.index(' 1')+2], Data[Data.index(' 1')+3]);  k=1
                else: k=0
                if Data[1+4*k]==' 3':   Acelerometro.Actualizando(Data[2+4*k], Data[3+4*k], Data[4+4*k])
                if len(Data)>5 and Data[5+4*k]==4:    Grioscopio.Actualizando(Data[6+4*k], Data[7+4*k], Data[8+4*k])

                #print(Acelerometro.getdA()[-1])
                #plt.scatter(t,float(Acelerometro.getdA()[-1]))
                #plt.pause(0.001)
                #t+=1

                #--- Pruebas con el acelerometro lineal y la gravedad
                if Data.count(' 83')>0 and Data.count(' 82')>0:
                    grav=np.array([float(Data[Data.index(' 83')+1]),float(Data[Data.index(' 83')+2]),float(Data[Data.index(' 83')+3])])
                    acclin=np.array([float(Data[Data.index(' 82')+1]),float(Data[Data.index(' 82')+2]),float(Data[Data.index(' 82')+3])])
                    if np.linalg.norm(acclin)>tolgrav: #Prueba con gravity y vector aceleracion
                        coseno=np.dot(grav,acclin)/(np.linalg.norm(grav)*np.linalg.norm(acclin))
                        if coseno < -0.90:
                            caida=True
                            print("Caida! Coseno: "+ str(coseno)+ " norma: "+ str(np.linalg.norm(acclin)))
                #----Segundo Detector------
                if abs(Acelerometro.getdA()[-1]) > tolacel:
                    caida1 = True
                #--------Confirmacion de caida------------
                if caida and (not flag): # and caida1:
                    print("Atention, a fall has occured!")
                    #print(GPS.getY())
                    Email("Your grandparent has fallen at latitude {}, longitude {} and height  = {} the day {} at {} time. \n To locate this position go to https://www.gps-coordinates.net and enter the latitude and longitude".format(GPS.getX()[-1], GPS.getY()[-1], GPS.getZ()[-1], str(datetime.datetime.now().date()) , str(datetime.datetime.now().time())[:8]))
                    flag = True #Para no enviar mas correos
                #print(repr(keypressed))
                if keypressed=="x":
                    break
            except IOError:
                print('Not ready')


plt.show()
