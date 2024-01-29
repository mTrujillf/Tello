# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 21:14:00 2024

@author: Miguel
"""

import pygame

def init():
    pygame.init()
    win = pygame.display.set_mode((400,200))
    
def getKey(keyName):
    ans = False
    for eve in pygame.event.get():pass
    KeyInput = pygame.key.get_pressed()
    myKey = getattr(pygame,'K_{}'.format(keyName))
    
    if KeyInput[myKey]:
        ans = True
    pygame.display.update()
    
    
    return ans

