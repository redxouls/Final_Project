import sys, pygame
import numpy as np
from pygame.locals import *
from vpython import *

class Truss():
    def __init__(self,nodeA=None,nodeB=None,screen=None,*,pos=None,axis=None,radius=None):
        self.nodeA = nodeA
        self.nodeB = nodeB
        if self.nodeA!= None and self.nodeB != None:
            self.oril = mag(nodeA.pos-nodeB.pos)
        self.screen = screen
        self.maxforce = 100
        self.collided = False
        self.pos = pos
        self.axis = axis
        self.radius = radius
        self.collapse = False
        
    def draw_Truss(self,todel):
        screen = self.screen
        if todel:
            pygame.draw.line(self.screen,(230,230,230), self.nodeA.to_int(), self.nodeB.to_int(), 17)
        else:
            pygame.draw.line(self.screen,(204,102,0), self.nodeA.to_int(), self.nodeB.to_int(), 17)
    def draw_marked_Truss(self,todel):
        screen = self.screen
        if todel:
            pygame.draw.line(self.screen,(230,230,230), self.nodeA.to_int(), self.nodeB.to_int(), 17)
        else:
            pygame.draw.line(self.screen,(0,0,0), self.nodeA.to_int(), self.nodeB.to_int(), 17) 

    def damaged(self,force_ext):
        return self.maxforce>force_ext
    
    def length(self):
        return mag(self.nodeA.pos-self.nodeB.pos)
