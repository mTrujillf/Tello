# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 13:27:13 2024

@author: Miguel
"""

import libardrone
from time import sleep
import detectorTeclas as dt

dt.init()

def getKeyboradInput():
    if dt.getKey("k") :
        print("land")
        drone.land()
    if dt.getKey("h"):
        print("halt")
        drone.halt()
        exit(1)
    if dt.getKey("t"):
        print("Take off")
        drone.takeoff()
    if dt.getKey("r"):
        drone.reset()
         
drone = libardrone.ARDrone()
drone.takeoff()


while True:
    getKeyboradInput()

