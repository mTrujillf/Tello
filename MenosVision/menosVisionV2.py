
from djitellopy import Tello
import analisisImagenMenosVision as aI
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
        #file = open('vuelo.txt','w')
        #for item in todosRC:
        #    for rc in item:
        #        file.write(str(rc) + ",")
        #    file.write("\n")
        #file.write("Len:" + str(len(todosRC)))
        #file.close()
        tello.land()
        tello.streamoff()
        
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
tope = [600,150]
#600 funciono bien
todosRC = list()
dir_final= r'D:\Python\MenosVision\vuelo2Bien'
jpg = ".jpg"
#Control RC dependiendo de qué matriz fue máxima.
matRc = [[[0,15,7],[0,25,7],[0,33,7]],
         [[0,40,5],[0,45,5]],
         [[0,55,0],[0,60,0]],
         [[0,67,0],[0,74,0]],
         [[0,-15,-7],[0,-25,-7],[0,-33,-7]],
         [[0,-40,-5],[0,-45,-5]],
         [[0,-55,0],[0,-60,0]],
         [[0,-67,0],[0,-74,0]]]

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
try:
    print(tello.get_battery())
    tello.takeoff()
    tello.send_rc_control(0, 0, 0, 0)
    tello.send_command_with_return("downvision 0")
    tello.send_command_with_return("downvision 1")
    tello.set_video_fps(Tello.FPS_5)
    tello.set_video_fps(Tello.FPS_30)
    img = tello.get_frame_read().frame
    #tello.move_up(20)
    #tello.move_down(25)
    sleep(2)
    sigue =True 
    
    matInicio = np.ones((240,320))
    
    while sigue:
        sigue = getKeyboradInput()
        img = tello.get_frame_read().frame
        bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        BW = aI.blackwhite(bw)
        der = sum(sum(BW[0:119,0:80]))
        izq = sum(sum(BW[120:239,0:90]))
        x = (der - izq)
        x = int(x/150)
        #print(x)
        tello.send_rc_control(x,-10, 0, 0)
        if abs(x) < 5 :
            sigue = False
        cv2.imshow("Img", img)
        cv2.waitKey(1)
     
        
    getKeyboradInput()#Detecta si se apretó alguna tecla para detener.
        
    tello.send_rc_control(0, 0, 0, 0)
    #arr = [0,0,0,0]
    #todosRC.append(arr)
    #Lectura y visualización de la imagen.
    img = tello.get_frame_read().frame
    img = img[39:199,59:299]
    bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    BW = aI.blackwhite(bw)
    cv2.imshow("Img", BW)
    cv2.waitKey(1)
        
    #Método que calcula el máximo de las matrices.
    i,k = aI.getTodo(BW,tope) 
    start = time.time_ns()
    #os.chdir(dir_final) 
    #os.listdir(dir_final)
    
    while True:
        getKeyboradInput()#Detecta si se apretó alguna tecla para detener.
    
        while i == 8:#caso 4x3
            getKeyboradInput()
            
            if time.time_ns() - start > 33000000:
                start = time.time_ns()
                img = tello.get_frame_read().frame
                bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                BW = aI.blackwhite(bw)
                
                enfrente = BW[90:149,0:40]
                sumEnfrente = sum(sum(enfrente))
                maxEnfrente = 2360.0
                potExtra = (sumEnfrente/maxEnfrente) * 5
                potExtra = int(potExtra)
                pitch = 10 + potExtra
                BW = BW[30:209,40:279]
                der = BW[49:89,0:70]
                izq = BW[90:130,0:70]
                centro = img[60:119,0:59]
                centroBW = BW[60:119,0:59] 
                #print("centro:    " + str(sum(sum(centroBW))))
                #Diferencia entre matrices para centrar la imagen.
                x = aI.centrar(BW)
            
                #yaw = int(x * 1.5 * signo)#Para subir un poco más la rotación de centrado.
                #if(abs(x[0])<10):
                roll = x[0]
                yaw = x[1]
                tello.send_rc_control(roll, pitch, 0, yaw)
                arr = [roll,pitch,0,yaw]
                #else:
                #    tello.send_rc_control(x[0], 15, 0, 0)
                #    arr = [x[0],15,0,0]
                #print(arr)
                todosRC.append(arr)
                #Mostrar imagen del drone.
                cv2.imshow("Img", BW)
                cv2.waitKey(1)
                i,k = aI.getTodo(BW,tope)
                #filename = "__________" + str(time.time()) + "___________"+ jpg
                #cv2.imwrite(filename, img)
            
    #        cont = cont + 1
        
    #    while i < 6:#caso 3x3
        tello.send_rc_control(0, 0, 0, 0)
        
        while i < 8:
            getKeyboradInput()
            if time.time_ns() - start > 33000000:
                start = time.time_ns()
                
                #Dependiendo de qué matriz salió máxima, se guardan los valores de RC.
                arrRc = matRc[i] 
                rc = arrRc[k]
                tello.send_rc_control(0, rc[0], 0, rc[1])#Mandar los valores de RC al drone.
                arr = [rc[2],rc[0],0,rc[1]]
                #print(arr)
                todosRC.append(arr)
                #Nueva imagen
                img = tello.get_frame_read().frame
                img = img[29:209,40:279]
                bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                BW = aI.blackwhite(bw)
            
                cv2.imshow("Img", BW)
                cv2.waitKey(1)
                i,k = aI.getTodo(BW,tope)
                #filename = "__________" + str(time.time()) + "___________"+ jpg
                #cv2.imwrite(filename, img)
        if i == 9:
            print("salio")
    #        cont = cont + 1
except:
    tello.land()