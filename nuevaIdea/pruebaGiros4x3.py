# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 07:40:58 2024

@author: Miguel
"""

from djitellopy import Tello
import analisisImagen4x3
from time import sleep
import cv2
import detectorTeclas as dt

#Método para detectar la entrada del teclado y detener el drone
def getKeyboradInput():
    if dt.getKey("k") : 
        tello.land()
        tello.streamoff()
        sleep(1)
        exit(1)
        
#Se refiere a la función que calcula el máximo de matrices. Si el valor de la 
#matriz de adelante es menor a 400, se revisa cuál de las matrices laterales es 
#la máxima y si es mayor a 200
tope = [400,200]

#Control RC dependiendo de qué matriz fue máxima.
arrRc = [[[7,15],[5,25],[3,33]],
         [[0,40],[0,45]],
         [[0,55],[0,60]],
         [[0,67],[0,74]],
         [[7,-15],[5,-25],[3,-33]],
         [[0,-40],[0,-45]],
         [[0,-55],[0,-60]],
         [[0,-67],[0,-74]]]

#Crea el objeto del drone.
tello = Tello()
 
#Inicio de detección de teclado.                
dt.init()

tello.connect()
tello.streamoff()
tello.streamon()


print(tello.get_battery())
tello.send_command_with_return("downvision 0")
tello.send_command_with_return("downvision 1")

img = tello.get_frame_read().frame

while True:
    getKeyboradInput()#Detecta si se apretó alguna tecla para detener.
    
    #Lectura y visualización de la imagen.
    img = tello.get_frame_read().frame
    bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    BW = analisisImagen4x3.blackwhite(bw)
    cv2.imshow("Bw", BW)
    cv2.waitKey(1)
    
    #Método que calcula el máximo de las matrices.
    i,k = analisisImagen4x3.getTodo(BW,tope) 

    while i == 8:
        getKeyboradInput()
        
        img = tello.get_frame_read().frame
        bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        BW = analisisImagen4x3.blackwhite(bw)

        #Mostrar imagen del drone.
        cv2.imshow("Bw", BW)
        cv2.waitKey(1)
        i,k = analisisImagen4x3.getTodo(BW,tope)
        
    while i < 8:
        
        getKeyboradInput()
        #Dependiendo de qué matriz salió máxima, se guardan los valores de RC.
        rc = arrRc[i,k] 
        print(rc)
        #Nueva imagen
        img = tello.get_frame_read().frame
        bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        BW = analisisImagen4x3.blackwhite(bw)
        
        cv2.imshow("Bw", BW)
        cv2.waitKey(1)
        i,k = analisisImagen4x3.getTodo(BW,tope)

    if i == 9:
        tello.streamoff()
        sleep(1)
        exit(1)















