import socket, os, datetime, smtplib
import matplotlib.pyplot as plt
import numpy as np
import msvcrt
print("Presione la tecla x para salir.")

#------------Clase-----------
class Sensor:
  def __init__(self):
    self.X=[]; self.Y=[]; self.Z=[]; self.A=[]; self.Angulo=[];

  def getX(self): return(self.X)
  def getY(self): return(self.Y)
  def getZ(self): return(self.Z)
  def getA(self): return(self.A)
  def getAngulo(self): return(self.Angulo)
  def Actualizando(self, x, y, z):
      self.X.append(float(x)); self.Y.append(float(y));
      self.Z.append(float(z)); self.A.append((float(x)**2+float(y)**2+float(z)**2)**0.5)
      if abs(float(x))>0.0001: self.Angulo.append(np.arctan(((float(y)**2 + float(z)**2)**0.5)/float(x)) * 180/np.pi) #Angulo theta, esfericas
      else: self.Angulo.append(90.)
###Se puede modificar la parte  de append para que las listas tengan una longitud constante###
#-----------Creando email-----------
def Email(body):
  gmail_user = 'iaun2019pe@gmail.com'
  gmail_password = 'Qwert54321'

  sent_from = gmail_user
  to = ['ddfulaa@unal.edu.co']
  subject = 'OMG Super Important Message'
   #body = 'Ohhhh my joint has fallen'

  email_text = """\
   From: %s
   To: %s
   Subject: %s

   %s
   """ % (sent_from, ", ".join(to), subject, body)

  server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
  server.ehlo()
  server.login(gmail_user, gmail_password)
  server.sendmail(sent_from, to, email_text)
  server.close()
  print ('Email sent!')


#-------------Creando conexion-------------------
UDP_IP_ADDRESS = "192.168.1.59"
UDP_PORT_NO = 5555

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

#--------------Tomando Datos---------------------------
flag= False
GPS = Sensor()
Gravedad = Sensor() #83
Aceleracion_lineal= Sensor() #82
caida=False
while True:
  if msvcrt.kbhit():
     key = msvcrt.getch().decode('utf-8')
     if key.lower()=='x':
         break
  data, addr = serverSock.recvfrom(8192)
  Data = data.decode("utf-8").split(",")   
  #--- Pruebas con el acelerometro lineal y la gravedad
  if Data.count(' 83')>0 and Data.count(' 82')>0:
    grav=np.array([float(Data[Data.index(' 83')+1]),float(Data[Data.index(' 83')+2]),float(Data[Data.index(' 83')+3])])
    acclin=np.array([float(Data[Data.index(' 82')+1]),float(Data[Data.index(' 82')+2]),float(Data[Data.index(' 82')+3])])
    if np.linalg.norm(acclin)>10:
      coseno=np.dot(grav,acclin)/(np.linalg.norm(grav)*np.linalg.norm(acclin))
      if coseno < -0.90:
        caida=True
        print("Caida! Coseno: "+ str(coseno)+ " norma: "+ str(np.linalg.norm(acclin)))
            
  if caida and not flag:
    print("Atencion, ha ocurrido una caida!")
    Email("Su madre")#Email("Se ha caido su abuelita en la posicion x = {}, y = {}, z = {} el dia {} a las {} horas".format(GPS.getX()[-1], GPS.getY()[-1], GPS.getZ()[-1], str(datetime.datetime.now().date()) , str(datetime.datetime.now().time())[:8]  ))
    flag = True #Para no enviar mas correos
 
serverSock.close()

