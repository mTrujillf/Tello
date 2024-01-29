# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 19:04:05 2024

@author: Miguel
"""
from djitellopy import Tello
import numpy as np
import math
import analisisImagen 
import time
from time import sleep
import cv2
import detectorTeclas as dt
import os


tello = Tello()

dt.init()

image_path_izq = r'D:/Python/Direccciones/Izq'

image_path_der = r'D:/Python/Direccciones/Der'

jpg = ".jpg"

def getKeyboradInput():
    if dt.getKey("k") : 
        tello.land()
        tello.streamoff()
        exit(1)
        
def calculaYaw(angulo):

    yaw_actual = tello.get_yaw()    

    yaw_final = yaw_actual + angulo
    
    if abs(yaw_final) >= 180:
        
        restante = 180 - abs(yaw_final)
        yaw_final = 180 - restante
        
        if yaw_final > 0:
            yaw_final = - 1 * yaw_final
        
        
    
    return yaw_final        

arrPi1 = [[((math.pi)/4),((math.pi)/8),((3 * math.pi)/8),((math.pi)/4)],
         [((7 * math.pi)/16),((3 * math.pi)/8),((9 * math.pi)/16),((5 * math.pi)/8)],
         [((5 * math.pi)/8),((3 * math.pi)/4),((3 * math.pi)/4),((7 * math.pi)/8)]]


arrPi2 = [[((math.pi)/8),((math.pi)/4),((math.pi)/4),((3 * math.pi)/8)],
         [((3 * math.pi)/8),((7 * math.pi)/16),((5 * math.pi)/8),((9 * math.pi)/16)],
         [((3 * math.pi)/4),((5 * math.pi)/8),((7 * math.pi)/7),((3 * math.pi)/4)]]
        

i = 10

tello.connect()
tello.send_rc_control(0, 0, 0, 0)
tello.streamon()
print(tello.get_battery())
tello.takeoff()
tello.send_command_with_return("downvision 0")
tello.send_command_with_return("downvision 1")
img = tello.get_frame_read().frame

sleep(3)
tello.move_up(20)
tello.move_down(30)

while i != 8:
    getKeyboradInput()
    tello.send_rc_control(0, 0, 0, 0)
    img = tello.get_frame_read().frame
    #    img = cv2.resize(img,(240,320))
    bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    BW = analisisImagen.blackwhite(bw)
    #Bw_rotate = cv2.rotate(BW, cv2.ROTATE_90_CLOCKWISE)
    cv2.imshow("Bw", BW)
    cv2.waitKey(1)
    
    i,v = analisisImagen.getToto(BW)
    
    while i == 7:
        getKeyboradInput()
        x = analisisImagen.centrar(BW)
        tello.send_rc_control(x, 13, 0, 0)
        img = tello.get_frame_read().frame
        bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        BW = analisisImagen.blackwhite(bw)
        #Bw_rotate = cv2.rotate(BW, cv2.ROTATE_90_CLOCKWISE)
        #cv2.imshow("Bw", Bw_rotate)
        cv2.imshow("Bw", BW)
        cv2.waitKey(1)
        i,v = analisisImagen.getToto(BW)
        
    if i < 7:
        tello.send_rc_control(0, 0, 0, 0)
        k = i % 3
                
        if i < 3:
            z = i + 1
            dir_final = image_path_der
            arrPiUtil = arrPi2[k]
            angulo = np.dot(v, arrPiUtil)
            angulo = angulo * 180 /math.pi
            tello.rotate_clockwise(int(angulo))
            filename = "der" + str(time.time()) + "___" + str(angulo) + jpg
                #            print("Gira Der")
        
        else:
            dir_final = image_path_izq
            arrPiUtil = arrPi1[k]
            angulo = np.dot(v, arrPiUtil)
            angulo = angulo * 180 /math.pi
            #            print("Gira Izq")
            tello.rotate_counter_clockwise(int(angulo))
            filename = "izq" + str(time.time()) + "___" + str(angulo)+ jpg
            #        print("Angulo: " + str(angulo))
        os.chdir(dir_final) 
        os.listdir(dir_final)
        cv2.imwrite(filename, img)
tello.streamoff()
tello.land()   




















