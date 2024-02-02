
import numpy as np

def blackwhite(img):
  
    channel3Min = 107.1
    channel3Max = 255.000
    
    BW = (img[:, :] >= channel3Min) & (img[:, :] <= channel3Max)

    BW = BW.astype(float)
    return BW    

def centrar(img):
    res = [0,0]
    der = sum(sum(img[70:119,45:105]))
    izq = sum(sum(img[120:169,45:105]))
    
    der1 = sum(sum(img[70:119,45:74]))
    izq1 = sum(sum(img[120:169,45:74]))
    der2 = sum(sum(img[70:119,75:105])) 
    izq2 = sum(sum(img[120:169,75:105]))
    
    x = der - izq
    
    x1 = der1 - izq1
    x2 = der2 - izq2
    signo = 1
    if abs(x1) > abs(x2):
        yaw = x1
    else:
        yaw = -x2
        
    res [0] = int( x/110)
    res[1] = int (yaw/45)
     
    return res
 
def getTodo(img,tope):
    i = 8
    k = 0
    
    #Pantallas central
    mat5 = img[80:159,0:79]
    
    sumMat5 = sum(sum(mat5))

    if sumMat5 < tope[0]:
        
        #Pantalla Der
        mat1 = img[0:79,0:79]
        mat2 = img[0:79,80:159]
        mat3 = img[0:79,160:239]
        mat4 = img[0:79,239:319]
        
        
        #Pantallas Izq
        mat6 = img[160:239,0:79]
        mat7 = img[160:239,80:159]
        mat8 = img[160:239,160:239]
        mat9 = img[160:239,240:319]
        
        sumMat1 = sum(sum(mat1))
        sumMat2 = sum(sum(mat2))
        sumMat3 = sum(sum(mat3))
        sumMat4 = sum(sum(mat4))
        
        sumMat6 = sum(sum(mat6))
        sumMat7 = sum(sum(mat7))
        sumMat8 = sum(sum(mat8))
        sumMat9 = sum(sum(mat9))
        
        todasSumMat = [sumMat1,sumMat2,sumMat3,sumMat4
                       ,sumMat6,sumMat7,sumMat8,sumMat9]
    
        sumMax = max(todasSumMat)

        j = np.array(todasSumMat).argmax()
        
        if sumMax >tope[1]:
            todasMat = [mat1,mat2,mat3,mat4,mat6,mat7,mat8,mat9]
            maxMat = todasMat[j]
            
            if j == 0:
                ventana1 = maxMat[0:39,0:39]
                ventana2 = maxMat[40:79,0:39]
                ventana3 = maxMat[0:39,40:79]
            
                sumVentana1 = sum(sum(ventana1))
                sumVentana2 = sum(sum(ventana2))
                sumVentana3 = sum(sum(ventana3))
            
                subVentanas = [sumVentana1,sumVentana2,sumVentana3]
                k = np.array(subVentanas).argmax()
                
            else:
                if j == 4:
                    ventana1 = maxMat[40:79,0:39]
                    ventana2 = maxMat[0:39,0:39]
                    ventana3 = maxMat[40:79,40:79]
            
                    sumVentana1 = sum(sum(ventana1))
                    sumVentana2 = sum(sum(ventana2))
                    sumVentana3 = sum(sum(ventana3))
            
                    subVentanas = [sumVentana1,sumVentana2,sumVentana3]
                    k = np.array(subVentanas).argmax()
                else:
                    if j < 4:
                    
                        ventana1 = maxMat[0:39,0:39]
                        ventana2 = maxMat[0:39,40:79]
            
                        sumVentana1 = sum(sum(ventana1))
                        sumVentana2 = sum(sum(ventana2))
            
                        subVentanas = [sumVentana1,sumVentana2]
                        k = np.array(subVentanas).argmax()
                    else:
                        ventana1 = maxMat[40:79,0:39]
                        ventana2 = maxMat[40:79,40:79]
            
                        sumVentana1 = sum(sum(ventana1))
                        sumVentana2 = sum(sum(ventana2))
            
                        subVentanas = [sumVentana1,sumVentana2]
                        k = np.array(subVentanas).argmax()
                        
            i = j 
        else:
            i = 9
    return i, k
    





















