import socket, os, datetime, smtplib
import matplotlib.pyplot as plt

#------------Clase-----------
class Sensor:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
    self.Amplitud = (x**2+y**2+z**2)**0.5
    self.X=[]; self.Y=[]; self.Z=[]; self.A=[]
  def Actualizando(self):
      self.X.append(self.x); self.Y.append(self.y);
      self.Z.append(self.z); self.A.append(self.Amplitud)

Acelerometro = Sensor(0,4,3)
Acelerometro.X.append(2)
print(Acelerometro.X)

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

#------------Funciones-------------------------
def StrToFloat(A):
 for i in range(len(A)): A[i]=float(A[i])
self.X=[]

def Magnitud(A): return(round((A[0]**2+A[1]**2+A[2]**2)**0.5,2))

def angulo(A):
    return round(np.arctan(((A[1]**2 + A[2]**2)**0.5)/A[0]) * 180/np.pi,2)

def diferencias(X,Y,Z,i):
    return (round(((Y[i+1]-Y[i])**2+(Z[i+1]-z[i])**2+(X[2])**2)**0.5,2))

#-------------Creando conexion-------------------
UDP_IP_ADDRESS = "192.168.1.7"
UDP_PORT_NO = 5550

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

#--------------Tomando Datos---------------------------
Acelerometro = Sensor(1,2,3)
Grioscopio= Sensor(1,2,3)


Tiempo, Acelerometro, Giroscopio, Magnetico, GPS = [],[],[],[],[] #Listas de posicion
dt=0.01 #Distancia entre datos
tolacel, tolgir= 2, 20  #newtons, no se
flat= False
GPS=[0,0,0]

for i in range(100):

   data, addr = serverSock.recvfrom(1024)
   Data = data.decode("utf-8").split(",")

   StrToFloat(Data)

   Tiempo.append(float(Data[0]))
   if len(Data)>14 and Data[1]==1: GPS=Data[2:5]; k=1
   else: k=0
   if Data[1+4*k]==3:   A=Data[2+4*k:5+4*k]; Acelerometro.append(Magnitud(A))
   if len(Data)>5 and Data[5+4*k]==4:    A=Data[6+4*k:9+4*k]; Giroscopio.append(Magnitud(A))
   #if len(Data)>10 and Data[9+4*k]==5:    A=Data[10+4*k:13+4*k]; Magnetico.append(Magnitud(A))

   if i>0 and (Acelerometro[i]-Acelerometro[i-1]>tolacel) and len(GPS)!=0 and flat == False: # and #or Giroscopio[i]-Giroscopio[i-1]>tolgir) and
#     print("se cayo", Data[0]);
     Email("Se ha caido su abuelita en x = {}, y = {}, z = {} el dia {} a las {} horas".format(GPS[0], GPS[1], GPS[2],str(datetime.datetime.now().date()) , str(datetime.datetime.now().time())[:8]  ))
     flat = True #Para no enviar mas correos


   print("Datos:", data, len(data))
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
