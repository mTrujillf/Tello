# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 17:32:13 2024

@author: Miguel
"""
import numpy as np
import cv2
#imagen BW 320,240
#def __init__():



def blackwhite(img):

#    channel1Min = 0.000
#    channel1Max = 255.000
    
#    channel2Min = 0.000
#    channel2Max = 255.000
    
    channel3Min = 107.1
    channel3Max = 255.000
    
    BW = (img[:, :] >= channel3Min) & (img[:, :] <= channel3Max)
    
    #BW = (
    #(img[:, :] >= channel1Min) & (img[:, :] <= channel1Max) &
    #(img[:, :] >= channel2Min) & (img[:, :] <= channel2Max) &
    #(img[:, :] >= channel3Min) & (img[:, :] <= channel3Max)
    #)
    
    BW = BW.astype(float)
    return BW    

def centrar(img):
    
    der = sum(sum(img[80:119,10:30]))
    izq = sum(sum(img[120:159,10:30]))
    
    x = der - izq
    res = x/80
     
    return int(res)
 
def getToto(img):
    i = 7
    sumVentanas = []
    #print(img.shape)
    #x,y = img.shape
    #print("x: " + str(x))
    #print("y: " + str(y))
    #print(img)
    #print(sum(img))
    #print('-----------------------------------------------------')
    #arr = img[0:10,0:10]
    #print(arr)
    #print("z: " + str(z))
    #Pantallas Izq
    #mat1 = img[0:106,0:79]
    #mat2 = img[106:212,0:79]
    #mat3 = img[213:319,0:79]
    
    #Pantallas central
    #mat4 = img[0:106,80:159]

    #Pantallas Der
    #mat5 = img[0:106,160:239]
    #mat6 = img[106:212,160:239]
    #mat7 = img[213:319,160:239]
    
    mat1 = img[0:79,0:106]
    mat2 = img[0:79,106:212]
    mat3 = img[0:79,213:319]
    
    #Pantallas central
    mat4 = img[80:159,0:106]

    #Pantallas Der
    mat5 = img[160:239,0:106]
    mat6 = img[160:239,106:212]
    mat7 = img[160:239,213:319]
    
    
    #cv2.imshow("mat1", mat1)
    #cv2.imshow("mat2", mat2)
    #cv2.imshow("mat3", mat3)
    #cv2.imshow("mat4", mat4)
    #cv2.imshow("mat5", mat5)
    #cv2.imshow("mat6", mat6)
    #cv2.imshow("mat7", mat7)
    
    #cv2.waitKey(0)
    
    sumMat4 = sum(sum(mat4))
    #print("SumMat4: " + str(sumMat4))
    if sumMat4 < 400:
        sumMat1 = sum(sum(mat1))
        sumMat2 = sum(sum(mat2))
        sumMat3 = sum(sum(mat3))
        sumMat5 = sum(sum(mat5))
        sumMat6 = sum(sum(mat6))
        sumMat7 = sum(sum(mat7))
        
        todasSumMat = [sumMat1,sumMat2,sumMat3,sumMat5,sumMat6,sumMat7]
    
        sumMax = max(todasSumMat)
        #print("sumMax:" + str(sumMax))
        j = np.array(todasSumMat).argmax()
        
        if sumMax >200:
            todasMat = [mat1,mat2,mat3,mat5,mat6,mat7]
            maxMat = todasMat[j]
            
            #ventana1 = maxMat[0:53,0:39]
            #ventana2 = maxMat[0:53,40:79]
            #ventana3 = maxMat[54:106,0:39]
            #ventana4 = maxMat[54:106,40:79]
            
            ventana1 = maxMat[0:39,0:53]
            ventana2 = maxMat[40:79,0:53]
            ventana3 = maxMat[0:39,54:106]
            ventana4 = maxMat[40:79,54:106]
            
            #print(ventana1)
            #print(ventana2)
            #print(ventana3)
            #print(ventana4)
            #print(j)
            sumVentana1 = sum(sum(ventana1))
            sumVentana2 = sum(sum(ventana2))
            sumVentana3 = sum(sum(ventana3))
            sumVentana4 = sum(sum(ventana4))
            
            sumVentanas = [sumVentana1,sumVentana2,sumVentana3,sumVentana4]
            totSumVentanas = sum(sumVentanas)
            sumVentanas = [sumVentana1/totSumVentanas,sumVentana2/totSumVentanas,sumVentana3/totSumVentanas,sumVentana4/totSumVentanas]
            i = j 
        else:
            i = 8
    return i, sumVentanas 
    





















