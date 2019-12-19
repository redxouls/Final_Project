import sys, pygame
import numpy as np
from pygame.locals import *

class Node :
    def __init__(self,x=0,y =0,screen=None):
        self.x = x
        self.y = y
        self.cod = [self.x,self.y]
        self.r = 10
        self.screen = screen
    def draw_node(self):
        screen = self.screen
        pygame.draw.circle(screen, (0, 127, 255), self.to_int(), self.r, 0)
        return 
    def change_cod(self,newcod):
        self.x = newcod[0]
        self.y = newcod[1]
        self.cod = (self.x,self.y)
        return 
    def clicked(self,mouse_pos):
        distance = ((self.x-mouse_pos[0])**2+(self.y-mouse_pos[1])**2)**0.5
        if distance <= self.r:
            return True
        else:
            return False
    def to_int(self):
        return int(self.cod[0]), int(self.cod[1])
class Truss(Node):
    def __init__(self,nodeA=None,nodeB=None,screen=None):
        self.nodeA = nodeA
        self.nodeB =nodeB
        self.screen = screen
    
    def draw_Truss(self):
        screen = self.screen
        pygame.draw.line(self.screen,(0,0,0), self.nodeA.to_int(), self.nodeB.to_int(), 5)
