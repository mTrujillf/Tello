# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 11:52:51 2024

@author: Miguel
"""

from djitellopy import Tello
import analisisImagen 
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
arrRc = [[5,25],[2,35],[0,60],[5,-25],[0,-50],[-5,-60]]

#Crea el objeto del drone.
tello = Tello()
 
#Inicio de detección de teclado.                
dt.init()

#Inicio de instrucciones para el drone.
tello.connect()
tello.send_rc_control(0, 0, 0, 0)
tello.streamoff()
tello.streamon()

print(tello.get_battery())
tello.takeoff()
tello.send_command_with_return("downvision 0")
tello.send_command_with_return("downvision 1")
tello.set_video_fps(Tello.FPS_5)
tello.set_video_fps(Tello.FPS_30)
img = tello.get_frame_read().frame

tello.move_up(20)
tello.move_down(25)



while True:
    getKeyboradInput()#Detecta si se apretó alguna tecla para detener.
    
    tello.send_rc_control(0, 0, 0, 0)
    
    #Lectura y visualización de la imagen.
    img = tello.get_frame_read().frame
    bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    BW = analisisImagen.blackwhite(bw)
    cv2.imshow("Bw", BW)
    cv2.waitKey(1)
    
    #Método que calcula el máximo de las matrices.
    i,v = analisisImagen.getTodo(BW,tope) 
    
    #While que se mantiene mientras la matriz de adelante sea mayor que el tope[0].
    while i == 7:
        getKeyboradInput()
        
        img = tello.get_frame_read().frame
        bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        BW = analisisImagen.blackwhite(bw)
        
        #Diferencia entre matrices para centrar la imagen.
        x = analisisImagen.centrar(BW)
        
        yaw = int(x * 1.5)#Para subir un poco más la rotación de centrado.
        tello.send_rc_control(x, 13, 0, yaw)

        #Mostrar imagen del drone.
        cv2.imshow("Bw", BW)
        cv2.waitKey(1)
        i,v = analisisImagen.getTodo(BW,tope)
    
    
    while i != 7:
        
        #Caso en el que solo se ve negro.
        if i == 8:
            tello.land()
            tello.streamoff()
            sleep(1)
            exit(1)
        
        
        getKeyboradInput()
        #Dependiendo de qué matriz salió máxima, se guardan los valores de RC.
        rc = arrRc[i] 
        tello.send_rc_control(0, rc[0], 0, rc[1])#Mandar los valores de RC al drone.
        
        #Nueva imagen
        img = tello.get_frame_read().frame
        bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        BW = analisisImagen.blackwhite(bw)
        
        cv2.imshow("Bw", BW)
        cv2.waitKey(1)
        i,v = analisisImagen.getTodo(BW,tope)
       