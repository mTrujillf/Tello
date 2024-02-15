# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 16:02:05 2024

@author: Miguel
"""
import matplotlib.pyplot as plt

arrTxt = list()

with open('vuelo.txt') as f:
    [arrTxt.append(line) for line in f.readlines()]

arrFinal = list()
for item in arrTxt:
    fields = item.split(",")
    arrFinal.append(fields)

zDes = list()
ze = list()
zDesdot = list()
z = list()
w = list()
t = list()

for dato in arrFinal:
    zDes.append(dato[0])
    ze.append(dato[1])  
    zDesdot.append(dato[2])
    z.append(dato[3])
    w.append(dato[4])
    t.append(dato[5])
    

#print(t)
print(len(t))
plt.plot(zDes,'ro')
plt.show()
print(len(t))