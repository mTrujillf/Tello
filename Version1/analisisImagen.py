# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 17:32:13 2024

@author: Miguel
"""
import numpy as np

def blackwhite(img):
  
    channel3Min = 107.1
    channel3Max = 255.000
    
    BW = (img[:, :] >= channel3Min) & (img[:, :] <= channel3Max)

    BW = BW.astype(float)
    return BW    

def centrar(img):
    
    der = sum(sum(img[70:119,25:65]))
    izq = sum(sum(img[120:169,25:65]))
    
    x = der - izq
    res = x/110
     
    return int(res)
 
def getTodo(img,tope):
    i = 7
    sumVentanas = []
    
    mat1 = img[0:79,0:106]
    mat2 = img[0:79,106:212]
    mat3 = img[0:79,213:319]
    
    #Pantallas central
    mat4 = img[80:159,0:106]

    #Pantallas Der
    mat5 = img[160:239,0:106]
    mat6 = img[160:239,106:212]
    mat7 = img[160:239,213:319]
    
    sumMat4 = sum(sum(mat4))

    if sumMat4 < tope[0]:
        sumMat1 = sum(sum(mat1))
        sumMat2 = sum(sum(mat2))
        sumMat3 = sum(sum(mat3))
        sumMat5 = sum(sum(mat5))
        sumMat6 = sum(sum(mat6))
        sumMat7 = sum(sum(mat7))
        
        todasSumMat = [sumMat1,sumMat2,sumMat3,sumMat5,sumMat6,sumMat7]
    
        sumMax = max(todasSumMat)

        j = np.array(todasSumMat).argmax()
        
        if sumMax >tope[1]:
            todasMat = [mat1,mat2,mat3,mat5,mat6,mat7]
            maxMat = todasMat[j]
            
            ventana1 = maxMat[0:39,0:53]
            ventana2 = maxMat[40:79,0:53]
            ventana3 = maxMat[0:39,54:106]
            ventana4 = maxMat[40:79,54:106]
            
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
    





















