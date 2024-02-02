# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 11:09:30 2024

@author: Miguel
"""

items = [[0,0,0,0], [7,8,0,7], [0,15,0,0], [5,6,7,8]]
file = open('vuelo1.txt','w')
for item in items:
    for rc in item:
        file.write(str(rc) + ",")
    file.write("\n")
file.close()