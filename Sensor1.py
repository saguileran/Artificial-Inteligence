import socket, os, datetime, smtplib
import matplotlib.pyplot as plt
import numpy as np

#------------Clase-----------
class Sensor:
  def __init__(self):
<<<<<<< HEAD
    self.X=[];  self.Y=[];  self.Z=[];  self.A=[];  self.Angulo=[]
    self.dX=[]; self.dY=[]; self.dZ=[]; self.dA=[]; self.dAngulo=[]

  def getX(self): return(self.X);
  def getdX(self): return(self.dX);
  def getY(self): return(self.Y);
  def getdY(self): return(self.dY);
  def getZ(self): return(self.Z);
  def getdZ(self): return(self.dZ);
  def getA(self): return(self.A);
  def getdA(self): return(self.dA);
  def getAngulo(self): return(self.Angulo);
  def getdAngulo(self): return(self.dAngulo);


  def Actualizando(self, x, y, z):
    x,y,z = float(x), float(y), float(z)
    self.X.append(x);      self.Y.append(y);      self.Z.append(z);
    self.A.append((x**2+y**2+z**2)**0.5)
    self.Angulo.append(np.arccos(z/(y**2 + z**2+x**2)**0.5) * 180/np.pi) #Angulo theta de esfericas en grados
    #if abs(x)>0.0001: self.Angulo.append(np.arctan(((y**2 + z**2)**0.5)/x) * 180/np.pi) #Angulo theta, esfericas
    if len(self.X)>1:
      self.dX.append(self.X[-1]-self.X[-2])
      self.dY.append(self.Y[-1]-self.Y[-2])
      self.dZ.append(self.Z[-1]-self.Z[-2])
      self.dA.append(self.A[-1]-self.A[-2])
      self.dAngulo.append(self.Angulo[-1]-self.Angulo[-2])
=======
    self.X=[]; self.Y=[]; self.Z=[]; self.A=[]; self.Angulo=[]; self.difX=[]; self.difY=[]; self.difZ=[]; self.difAngulo=[];

  def getX(self): return(self.X)
  def getY(self): return(self.Y)
  def getZ(self): return(self.Z)
  def getA(self): return(self.A)
  def getAngulo(self): return(self.Angulo)
  def getdifX(self): return(self.difX)
  def getdifY(self): return(self.difY)
  def getdifZ(self): return(self.difZ)
  def getdifAngulo(self): return(self.difAngulo)

  def Actualizando(self, x, y, z):
      self.X.append(float(x)); self.Y.append(float(y));
      self.Z.append(float(z)); self.A.append((float(x)**2+float(y)**2+float(z)**2)**0.5)
      if abs(float(x))>0.0001: self.Angulo.append(np.arctan(((float(y)**2 + float(z)**2)**0.5)/float(x)) * 180/np.pi) #Angulo theta, esfericas
      else: self.Angulo.append(90.)
      if len(self.X)>1: self.difX.append(self.X[-1]-self.X[-2]); self.difY.append(self.Y[-1]-self.Y[-2]); self.difZ.append(self.Z[-1]-self.Z[-2]); self.difAngulo.append(self.Angulo[-1]-self.Angulo[-2]);
  
  def AcumuladorDeDiferencias(self, n): #El n nos indica la cantidad de puntos que se van a considerar para calcular las diferencias
    if len(self.difX)>=n:
        return [sum(self.difX[len(self.difX)-n-1:len(self.difX)-1]), sum(self.difY[len(self.difY)-n-1:len(self.difY)-1]), sum(self.difZ[len(self.difZ)-n-1:len(self.difZ)-1]), sum(self.difAngulo[len(self.difAngulo)-n-1:len(self.difAngulo)-1])]        
    else:
        return [sum(self.difX), sum(self.difY), sum(self.difZ), sum(self.difAngulo)]
>>>>>>> 9fea3d6badd9cb4547ca765611b109caf4e96c08

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

#------------Funciones-------------------------

#  if label==0: return (instanciaSensor.X[-1]-instanciaSensor.X[-2])
#  if label==1: return (instanciaSensor.Y[-1]-instanciaSensor.Y[-2])
#  if label==2: return (instanciaSensor.Z[-1]-instanciaSensor.Z[-2])
#  if label==3: return (instanciaSensor.Angulo[-1]-instanciaSensor.Angulo[-2])

#-------------Creando conexion-------------------
<<<<<<< HEAD
UDP_IP_ADDRESS = "192.168.1.14";    UDP_PORT_NO = 5555
=======
UDP_IP_ADDRESS = "192.168.1.59"
UDP_PORT_NO = 5555
>>>>>>> 9fea3d6badd9cb4547ca765611b109caf4e96c08

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

#--------------Tomando Datos---------------------------
#dt=0.01 #Distancia entre datos
tolang, toldif = 5, 5
<<<<<<< HEAD
NoDatos = 10**4
=======

>>>>>>> 9fea3d6badd9cb4547ca765611b109caf4e96c08
flag= False

GPS = Sensor();   Acelerometro = Sensor();   Giroscopio = Sensor();

<<<<<<< HEAD
for i in range(NoDatos):
=======
for i in range(200):
>>>>>>> 9fea3d6badd9cb4547ca765611b109caf4e96c08

   data, addr = serverSock.recvfrom(1024)
   Data = data.decode("utf-8").split(",")
#   print(Data)

   #Tiempo.append(float(Data[0]))

   if len(Data)>14 and Data[1]==' 1':    GPS.Actualizando(Data[2], Data[3], Data[4]);  k=1
   else: k=0
   if Data[1+4*k]==' 3':   Acelerometro.Actualizando(Data[2+4*k], Data[3+4*k], Data[4+4*k])
   if len(Data)>5 and Data[5+4*k]==4:    Grioscopio.Actualizando(Data[6+4*k], Data[7+4*k], Data[8+4*k])
<<<<<<< HEAD
#   Dif = list(Diferencias(Acelerometro))
#   print(Acelerometro.getdX())
 #  print("")
#   if (Dif[2]>toldif or abs(Dif[3])>tolang)  and flag == False: 
#     print("se cayo", Data[0]);
  #   Email("Se ha caido su abuelita en x = {}, y = {}, z = {} el dia {} a las {} horas".format(GPS[0], GPS[1], GPS[2], str(datetime.datetime.now().date()) , str(datetime.datetime.now().time())[:8]  ))
  #   flat = True #Para no enviar mas correos
=======
   print(Acelerometro.AcumuladorDeDiferencias(20))
   if Acelerometro.AcumuladorDeDiferencias(20)[2] > toldif and abs(Acelerometro.AcumuladorDeDiferencias(10)[3]) > tolang  and flag == False: 
     print("Atencion, ha ocurrido una caida!")
     Email("Se ha caido su abuelita en la posicion x = {}, y = {}, z = {} el dia {} a las {} horas".format(GPS.getX()[-1], GPS.getY()[-1], GPS.getZ()[-1], str(datetime.datetime.now().date()) , str(datetime.datetime.now().time())[:8]  ))
     flag = True #Para no enviar mas correos
>>>>>>> 9fea3d6badd9cb4547ca765611b109caf4e96c08

#print("Datos:", Acelerometro.getAngulo()) #, GPS.getY(), GPS.getZ())
#print(" ")

serverSock.close()

#-----------------------Graficando------------------------
Tiempo = np.arange(len(Acelerometro.getdX()))
fig, ax = plt.subplots(1, figsize=(8, 6))
ax.set_ylim([0,20])
#ax.plot(Tiempo, Acelerometro.getdX(), color="red", label="x")
#ax.plot(Tiempo, Acelerometro.getdY(), color="blue", label="y")
#ax.plot(Tiempo, Acelerometro.getdZ(), color="green", label="z")
ax.plot(Tiempo, Acelerometro.getAngulo(), 'bo', color="black", label="A")
#ax.plot(Tiempo, Giroscopio,'bo', color="blue", label="y")
#ax.plot(Tiempo, Magnetico,'bo', color="yellow", label="z")

ax.legend(loc="upper left", title="Aceleraciones", frameon=True)
plt.savefig('Aceleraciones.jpg')
plt.show()
#'''
