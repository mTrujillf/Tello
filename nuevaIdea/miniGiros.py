

from djitellopy import Tello
import analisisImagen4x3 as aI
from time import sleep
import cv2
import detectorTeclas as dt
import time
import numpy as np
import os
#Método para detectar la entrada del teclado y detener el drone
def getKeyboradInput():
    if dt.getKey("k") :
        cv2.destroyAllWindows()
        tello.land()
        tello.streamoff()
        #file = open('vuelo.txt','w')
        #for item in todosRC:
        #    for rc in item:
        #        file.write(str(rc) + ",")
        #    file.write("\n")
        #file.write("Len:" + str(len(todosRC)))
        #file.close()
        exit(1)
    
    if dt.getKey("i"):
        cv2.imshow("Img", matInicio)
        cv2.waitKey(3)
        return False
    
    return True
#Se refiere a la función que calcula el máximo de matrices. Si el valor de la 
#matriz de adelante es menor a 400, se revisa cuál de las matrices laterales es 
#la máxima y si es mayor a 200
#tope = [400,200]#caso 3x3
tope = [300,150]
todosRC = list()
dir_final= r'D:\Python\nuevaIdea\fotosVuelo2'
jpg = ".jpg"
#Control RC dependiendo de qué matriz fue máxima.
matRc = [[[0,15],[0,25],[0,33]],
         [[0,40],[0,45]],
         [[0,55],[0,60]],
         [[-5,67],[-5,74]],
         [[0,-15],[0,-25],[0,-33]],
         [[0,-40],[0,-45]],
         [[0,-55],[0,-60]],
         [[-5,-67],[-5,-74]]]
#matRc = [[[0,15],[0,25],[0,33]],
#         [[0,45],[0,55]],
#         [[0,67],[0,74]],
#         [[0,-15],[0,-25],[0,-33]],
#         [[0,-45],[0,-55]],
#         [[-5,-67],[-5,-74]]]

#Crea el objeto del drone.
tello = Tello()
 
#Inicio de detección de teclado.                
dt.init()

#Inicio de instrucciones para el drone.
tello.connect()
tello.send_rc_control(0, 0, 0, 0)
tello.streamoff()
tello.streamon()
cont = 0
print(tello.get_battery())
tello.takeoff()
tello.send_command_with_return("downvision 0")
tello.send_command_with_return("downvision 1")
tello.set_video_fps(Tello.FPS_5)
tello.set_video_fps(Tello.FPS_30)
img = tello.get_frame_read().frame
#tello.move_up(20)
#tello.move_down(15)
sleep(2)
sigue =True 

matInicio = np.ones((240,320))
#while sigue:
#    sigue = getKeyboradInput()
#    img = tello.get_frame_read().frame
#    cv2.imshow("Img", img)
#    cv2.waitKey(1)
 
    
getKeyboradInput()#Detecta si se apretó alguna tecla para detener.
    
tello.send_rc_control(0, 0, 0, 0)
#arr = [0,0,0,0]
#todosRC.append(arr)
#Lectura y visualización de la imagen.
img = tello.get_frame_read().frame
bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
BW = aI.blackwhite(bw)
cv2.imshow("Img", BW)
cv2.waitKey(1)
    
#Método que calcula el máximo de las matrices.
i,k = aI.getTodo(BW,tope) 
#start = time.time_ns()
#os.chdir(dir_final) 
#os.listdir(dir_final)

while True:
    getKeyboradInput()#Detecta si se apretó alguna tecla para detener.

    while i == 8:#caso 4x3
        
        getKeyboradInput()
        img = tello.get_frame_read().frame
        bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        BW = aI.blackwhite(bw)
        der = BW[70:119,45:105]
        izq = BW[120:169,45:105]
        #Diferencia entre matrices para centrar la imagen.
        x = aI.centrar(BW)
    
        #yaw = int(x * 1.5 * signo)#Para subir un poco más la rotación de centrado.
        if(abs(x[0]<10)):
            tello.send_rc_control(x[0], 10, 0, x[1])
            arr = [x[0],13,0,[1]]
        else:
            tello.send_rc_control(x[0], 10, 0, 0)
            arr = [x[0],13,0,0]
        todosRC.append(arr)
        #Mostrar imagen del drone.
        cv2.imshow("Img", BW)
        cv2.imshow("Der",der)
        cv2.imshow("Izq", izq)
        cv2.moveWindow("Der", 50, 400)
        cv2.moveWindow("Izq", 50, 520)
        cv2.waitKey(1)
        i,k = aI.getTodo(BW,tope)
        #filename = "_________" + str(time.time()) + "________________"+ jpg
        #cv2.imwrite(filename, img)
#        start = time.time_ns()
#        cont = cont + 1
    
#    while i < 6:#caso 3x3
    while i < 8:

        getKeyboradInput()
        #Dependiendo de qué matriz salió máxima, se guardan los valores de RC.
        arrRc = matRc[i] 
        rc = arrRc[k]
        tello.send_rc_control(0, rc[0], 0, rc[1])#Mandar los valores de RC al drone.
        arr = [0,rc[0],0,rc[1]]
        todosRC.append(arr)
        #Nueva imagen
        img = tello.get_frame_read().frame
        bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        BW = aI.blackwhite(bw)
    
        cv2.imshow("Img", BW)
        cv2.waitKey(1)
        i,k = aI.getTodo(BW,tope)
        #filename = "_________" + str(time.time()) + "________________"+ jpg
        #cv2.imwrite(filename, img)
#        start = time.time_ns()
#        cont = cont + 1