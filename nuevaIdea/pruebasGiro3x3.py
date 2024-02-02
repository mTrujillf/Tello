
from djitellopy import Tello
import analisisImagen3x3
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
tope = [200,50]

#Control RC dependiendo de qué matriz fue máxima.
matRc = [[[7,15],[5,25],[3,33]],
         [[0,45],[0,55]],
         [[0,67],[0,74]],
         [[7,-15],[5,-25],[3,-33]],
         [[0,-45],[0,-55]],
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
tello.set_video_fps(Tello.FPS_5)
tello.set_video_fps(Tello.FPS_30)

img = tello.get_frame_read().frame
sleep(2)
while True:
    getKeyboradInput()#Detecta si se apretó alguna tecla para detener.
    
    #Lectura y visualización de la imagen.
    img = tello.get_frame_read().frame
    bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    BW = analisisImagen3x3.blackwhite(bw)
    cv2.imshow("Bw", BW)
    cv2.waitKey(1)
    
    #Método que calcula el máximo de las matrices.
    i,k = analisisImagen3x3.getTodo(BW,tope) 

    while i == 6:
        getKeyboradInput()
        
        img = tello.get_frame_read().frame
        bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        BW = analisisImagen3x3.blackwhite(bw)

        #Mostrar imagen del drone.
        cv2.imshow("Bw", BW)
        cv2.waitKey(1)
        i,k = analisisImagen3x3.getTodo(BW,tope)
        
    while i < 6:
        
        getKeyboradInput()
        #Dependiendo de qué matriz salió máxima, se guardan los valores de RC.
        arrRc = matRc[i] 
        rc = arrRc[k]
        print('-----------------------------------------')
        print(i)
        print(rc)
        #Nueva imagen
        img = tello.get_frame_read().frame
        bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        BW = analisisImagen3x3.blackwhite(bw)
        
        cv2.imshow("Bw", BW)
        cv2.waitKey(1)
        i,k = analisisImagen3x3.getTodo(BW,tope)

    if i == 7:
        tello.streamoff()
        sleep(1)
        exit(1)

















