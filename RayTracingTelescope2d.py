# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 16:02:02 2019

@author: Daniela Fernanda López Astorquiza

Trazador de rayos en un sistema optico que simula 
un telescopio Maksutov Cassegrain
"""

import numpy as np                 # Paquete de funciones
import matplotlib                  # Para las imagenes
import matplotlib.pyplot as plt    # Para graficar
from PIL import Image              # Imagen
from skimage import io

matplotlib.rcParams.update({'font.size': 10})  # plot size

Nombreimagen = "marte.jpg" # Ingrese la imagen a analizar

image = Image.open(Nombreimagen)


 #PARAMETROS___________________________________________________________
 #Los parametros esta en metros
       #indices
ni1 = 1.0 #indice del medio
nt1 = 1.6 #indice de la lente

        #Menisco
R1 =  0.5 #radio de la primer superficie
R2 =  0.5  #radio de la segunda superficie

P1 = (nt1-ni1)/R1   #Potencia refractora 1
P2 = (ni1-nt1)/R2   #Potencia refractora 2

    #Espejo primario concavo
Re = 0.5

 #Espejo secundario convexo
Re2= -1.5


        #Distancias
d21 = 0.2  #grosor de la lente
d32 = 0.2  #ditancia del medio
de  = 0.1  #distancia espejo primario
de2 = 0.2 #distancia espejo secundario

     #ocular Kellner (K) tipo I (lente simple plano convexa)

R22 = -0.0027     #radio de la primer superficie

d211 = 0.01 #grosor de la lente
d322 = 0.01 #varia la distancia para el ocular

P22 = (ni1-nt1)/R22

#Rayos
dr = 0.004 #distancia entre los rayos paralelos
nr = 82    #número de rayos

n  = nr+1 # arreglo para que los rayos se distribuyan simetricos respecto al eje optico
 
lista = np.array(np.arange(-n/2+1,n/2))*dr #Alturas para hacer la lisya de rayos
#____________________________________________________________________________
#Para dibujar unas lienas que simbolizan la existencia de una superficie en el sistema óptico
def axes():
    plt.axvline(30, alpha=0.5, label="Lens")
    plt.axvline(50, alpha=0.5)
    plt.axvline(51, alpha=0.3)
    plt.axvline(120, alpha=0.3)
    plt.axvline(200, alpha=0.3)
    plt.axvline(210, alpha=0.3)
#___________________________________________________________________________    

 #TRATAMIENTO DE LOS RAYOS__________________________________________________ 
for yi1 in [lista]:
    #rayos incidentes que vienen desde el infinito
    yt1 = yi1      #yi1 me da las alturas de entrada
    alphat1 = -yi1*P1/nt1 
    #los rayos inciden en un menisco divergente
    yi2 = d21*alphat1+yt1
    alphai2 = (nt1/nt1)*alphat1
    
    yt2 = yi2
    alphat2=(nt1/ni1)*alphai2+(-P2*yi2)/ni1
    
    #rayos que se propagan en el medio despues del menisco
    yi3 = (d32/ni1)*ni1*alphat2+yt2
    alphai3 = (ni1/ni1)*alphat2
    
    #rayos que inciden en el espejo primario y se reflejasn
    yr1=yi3
    alphar1=alphai3-(2/Re)*yi3
    
    yet1= de*alphar1+yr1
    alphaet1=alphar1
    
    #rayos que inciden en el espejo secundario y se reflejan
    yr2=yet1
    alphar2=alphaet1-(2/Re2)*yet1
    
    yet2=de2*alphar2+yr2  #yet2 me da las alturas de salida antes de llegar al ocular
    alphaet2=alphar2
    
#    #ocular Kellner (K) tipo I (lente simple plano convexa)
    yt11 = yet2
    alphat11 = (ni1/nt1)*alphaet2
    
    yi22 = d211*alphat11+yt11
    alphai22 = (nt1/nt1)*alphat11
    
    yt22 = yi22
    alphat22=(nt1/ni1)*alphai22-P22*yt22/ni1
    
    #Rayos que se propagan despues del ocular
    
    yi33 = (d322/ni1)*ni1*alphat22+yt22 #alturas de salida después de pasar por el ocular

      #Lista de datos obtenidos de las ecuaciones
    # y almacena las alturas de los rayos encontradas
    y=[yi1,yt1,yi2,yt2,yi3,yet1,yet2,yt11,yi22,yi33]
    # x contiene unas posiciones simbolicas con el fin de observar el 
    # trazado de rayos, las verdaderas distancias entre los sistemas opticos 
    # se encuentran establecidas en los parametros
    x=[0, 30, 50, 50,120,  51, 170, 200, 210, 350]
    axes()
    plt.plot(x,y,"y", alpha=0.5)
    plt.title("Telescope ray tracing - Python")
    plt.xlabel("Lens position")
    plt.ylabel("Height of light rays [m]")
    plt.legend()
    
#___#Magnificación: "aumento transversal" sin ocular____
#    M = yet2/yi1
#    plt.plot(yet2,M)
#    plt.xlabel("Altura de la imagen [m]")
#    plt.ylabel("Aumento")
#    plt.ylim(-0.04,0.0)
#    print(M)


M = yet2[1]/yi1[1]  #Aumento transversal
print("Aumento transversal")
print(M)
    
#_____________________________________________________________________________
# Desarrollo teórico
#Imagen para definir a y b, primero encontrar las dimensiones de la imagen
imag=io.imread(Nombreimagen)/255.0 
#    print("- Dimensiones de la imagen:")
#    print(imag.shape) 
#    plt.imshow(imag,vmin=0,vmax=1)
#a corresponde al primer valor, b al segundo

a = imag.shape[0]
b = imag.shape[1]
#Imagen obtenida según los criterios de aumento transversal__________________
if (M < 0 and abs(M)<1):
    image     = image.rotate(180)  # rotacion
    width  = int(b*abs(M))
    height = int(a*abs(M))
    ima = image.resize((width, height), Image.BILINEAR) # aumento
    ext = ".jpg"
    ima.save("out" + ext)
