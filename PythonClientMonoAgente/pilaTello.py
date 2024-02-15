# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 13:03:47 2024

@author: Miguel
"""

from djitellopy import Tello

tello = Tello()
tello.connect()
print(tello.get_battery())