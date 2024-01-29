# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 19:04:05 2024

@author: Miguel
"""

from djitellopy import Tello
import numpy as np
import math
import analisisImagen 
from time import sleep
import cv2
import detectorTeclas as dt

tello = Tello()

dt.init()

def getKeyboradInput():
    if dt.getKey("k") : 
        tello.land()
        tello.streamoff()
        exit(1)
        
def calculaYaw(angulo):
    print(tello.get_yaw())
    yaw_actual = tello.get_yaw() 
    f = -1
    yaw_final = yaw_actual + angulo

    if abs(yaw_final) >= 180:
        restante = 180 - abs(yaw_final)
        yaw_final = 180 - abs(restante)
        f = 1
        if yaw_final > 0:
            yaw_final = - 1 * yaw_final
    
    return yaw_final , f        

tope = [400,200]

arrPi1 = [[((math.pi)/4),((math.pi)/8),((3 * math.pi)/8),((math.pi)/4)],
         [((7 * math.pi)/16),((3 * math.pi)/8),((9 * math.pi)/16),((5 * math.pi)/8)],
         [((5 * math.pi)/8),((3 * math.pi)/4),((3 * math.pi)/4),((7 * math.pi)/8)]]


arrPi2 = [[((math.pi)/8),((math.pi)/4),((math.pi)/4),((3 * math.pi)/8)],
         [((3 * math.pi)/8),((7 * math.pi)/16),((5 * math.pi)/8),((9 * math.pi)/16)],
         [((3 * math.pi)/4),((5 * math.pi)/8),((7 * math.pi)/7),((3 * math.pi)/4)]]

tello.connect()
#tello.send_rc_control(0, 0, 0, 0)
tello.streamon()
print(tello.get_battery())
#tello.takeoff()
try:
    tello.send_command_with_return("downvision 0")
    tello.send_command_with_return("downvision 1")
    img = tello.get_frame_read().frame
except:
    tello.land()
sleep(3)

tello.move_up(20)
tello.move_down(30)

sleep(3)

while True:
    getKeyboradInput()#teclado para detener
    
    tello.send_rc_control(0, 0, 0, 0)#control del drone
    
    #lectura y visualizacion de la imagen
    img = tello.get_frame_read().frame
    bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    BW = analisisImagen.blackwhite(bw)
    cv2.imshow("Bw", BW)
    cv2.waitKey(1)
    
    i,v = analisisImagen.getTodo(BW,tope) #
    
    while i == 7:
        getKeyboradInput()
        x = analisisImagen.centrar(BW)
        yaw = int(x * 75/50)
        tello.send_rc_control(x, 10, 0, yaw)
        img = tello.get_frame_read().frame
        bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        BW = analisisImagen.blackwhite(bw)
        
        #Bw_rotate = cv2.rotate(BW, cv2.ROTATE_90_CLOCKWISE)
        cv2.imshow("Bw", BW)
        cv2.waitKey(1)
        i,v = analisisImagen.getTodo(BW,tope)
        
    tello.send_rc_control(0, 0, 0, 0)
    k = i % 3
    if i < 7:            
        if i < 3:
            arrPiUtil = arrPi2[k]
            angulo = np.dot(v, arrPiUtil)
            angulo = int (angulo * 180 /math.pi)
    
        else:
            arrPiUtil = arrPi1[k]
            angulo = np.dot(v, arrPiUtil)
            angulo = int (-1 * angulo * 180 /math.pi)
                
        yaw_deseado,f = calculaYaw(angulo)
    
        if angulo < 0:
            num = -1
            if f == 1:
                yaw_deseado = yaw_deseado * -1
        else:
            num = 1
            if f == -1:
                yaw_deseado = yaw_deseado * -1
   
        dif = abs(yaw_deseado - tello.get_yaw())
        
        yaw = num * 20
        #tello.send_rc_control(0, 0, 0, yaw)
        
        while dif > 5  :
            tello.send_rc_control(0, 0, 0, yaw)
            getKeyboradInput()
            img = tello.get_frame_read().frame
            bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            BW = analisisImagen.blackwhite(bw)
            cv2.imshow("Bw", BW)
            cv2.waitKey(1)
            
            dif = abs(tello.get_yaw() - yaw_deseado)   




















