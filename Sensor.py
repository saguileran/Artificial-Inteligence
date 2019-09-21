import socket, os, datetime, smtplib
import matplotlib.pyplot as plt

#------------Clase-----------
class Sensor:
  def __init__(self):
    self.X=[]; self.Y=[]; self.Z=[]; self.A=[]

  def getX(self): return(self.X)
  def getY(self): return(self.Y)
  def getZ(self): return(self.Z)
  def getA(self): return(self.A)

  def Actualizando(self, x, y, z):
      self.X.append(float(x)); self.Y.append(float(y));
      self.Z.append(float(z)); self.A.append((float(x)**2+float(y)**2+float(z)**2)**0.5)
###Se puede modificar la parte  de append para que las listas tengan una longitud constante###

#-----------Creando email-----------
def Email(body):
   gmail_user = 'saguileran2@gmail.com'
   gmail_password = '961217.s'

   sent_from = gmail_user
   to = ['saguileran@unal.edu.co']
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
UDP_IP_ADDRESS = "192.168.1.112"
UDP_PORT_NO = 5550

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

#--------------Tomando Datos---------------------------
#dt=0.01 #Distancia entre datos
tolacel, tolgir= 2, 20  #newtons, no se
flat= False

GPS = Sensor()
Acelerometro = Sensor()
Giroscopio = Sensor()

for i in range(1000):

   data, addr = serverSock.recvfrom(1024)
   Data = data.decode("utf-8").split(",")
   #print(Data)

   #Tiempo.append(float(Data[0]))

   if len(Data)>14 and Data[1]==' 1':    GPS.Actualizando(Data[2], Data[3], Data[4]);  k=1
   else: k=0
   if Data[1+4*k]==' 3':   Acelerometro.Actualizando(Data[2+4*k], Data[3+4*k], Data[4+4*k])
   if len(Data)>5 and Data[5+4*k]==4:    Grioscopio.Actualizando(Data[6+4*k], Data[7+4*k], Data[8+4*k])
   #Sensor.Actualizando(Giroscopio)
  #if len(Data)>10 and Data[9+4*k]==5:    A=Data[10+4*k:13+4*k]; Magnetico.append(Magnitud(A))

#   if i>0 and (Acelerometro[i]-Acelerometro[i-1]>tolacel) and flat == False: # and #or Giroscopio[i]-Giroscopio[i-1]>tolgir) and
#     print("se cayo", Data[0]);
#     Email("Se ha caido su abuelita en x = {}, y = {}, z = {} el dia {} a las {} horas".format(GPS[0], GPS[1], GPS[2],str(datetime.datetime.now().date()) , str(datetime.datetime.now().time())[:8]  ))
#     flat = True #Para no enviar mas correos

   print("Datos:", GPS.getX(), GPS.getY(), GPS.getZ())
   print(" ")
#   print(" ")
#print("Tiempo: ", Tiempo);
#print("Acelrometro: ", Acelerometro);
#print("Giroscopio: ",Giroscopio);
#print("Magnetico: ",Magnetico);
#   print("GPS: ", GPS)

serverSock.close()
'''
#-----------------------Graficando------------------------
fig, ax = plt.subplots(1, figsize=(8, 6))
#ax.set_ylim([0,20])
ax.plot(Tiempo, Acelerometro, 'bo', color="red", label="x")
#ax.plot(Tiempo, Giroscopio,'bo', color="blue", label="y")
#ax.plot(Tiempo, Magnetico,'bo', color="yellow", label="z")

ax.legend(loc="lower right", title="Aceleraciones", frameon=True)

plt.show()'''
