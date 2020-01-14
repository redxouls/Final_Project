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
    def draw_obtruss(self):    
        screen = self.screen
        pygame.draw.line(self.screen,(30,170,30), self.nodeA.to_int(), self.nodeB.to_int(), 17) 

    def damaged(self,force_ext):
        return self.maxforce>force_ext
    
    def length(self):
        return mag(self.nodeA.pos-self.nodeB.pos)
    def truss_touch(self,other):
        px1 = (self.nodeA.pos.x,self.nodeB.pos.x-self.nodeA.pos.x)
        py1 = (self.nodeA.pos.y,self.nodeB.pos.y-self.nodeA.pos.y)
        px2 = (other.nodeA.pos.x,other.nodeB.pos.x-other.nodeA.pos.x)
        py2 = (other.nodeA.pos.y,other.nodeB.pos.y-other.nodeA.pos.y)
        a1 = px1[1]
        b1 = -px2[1]
        c1 = px2[0]-px1[0]
        a2 = py1[1]
        b2 = -py2[1]
        c2 = py2[0]-py1[0]
        delta = (a1*b2-a2*b1)
        if delta == 0:
            return True
        deltax = (c1*b2-c2*b1)
        deltay = (a1*c2-a2*c1)
        if 0 <= deltax/delta <= 1 and 0 <= deltay/delta <= 1:
            return True
        return False
