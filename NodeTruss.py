import sys, pygame
import numpy as np
from pygame.locals import *

class Node :
    def __init__(self,x=0,y =0,screen=None):
        self.x = x
        self.y = y
        self.cod = [x,y]
        self.r = 10
        self.screen = screen
    def draw_node(self):
        screen = self.screen
        pygame.draw.circle(screen, (0, 127, 255), self.cod, self.r, 0)
    def clicked(self,mouse_pos):
        distance = ((self.x-mouse_pos[0])**2+(self.y-mouse_pos[1])**2)**0.5
        if distance <= self.r:
            return True
        else:
            return False
class Truss(Node):
    def __init__(self,nodeA=None,nodeB=None,screen=None):
        self.nodeA = nodeA
        self.nodeB =nodeB
        self.screen = screen
    def draw_Truss(self):
        screen = self.screen
        pygame.draw.line(self.screen,(0,0,0), self.nodeA.cod, self.nodeB.cod, 3)
