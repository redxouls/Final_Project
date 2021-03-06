import sys, pygame
import numpy as np
from pygame.locals import *
from vpython import *

class Node :
    def __init__(self,x=0,y =0,screen=None,*,pos=None,radius=None):
        if pos == None:
            self.pos = vector(x,y,0)
        else:
            self.pos = pos
        self.radius = 15
        self.maxforce = 0.000000002
        self.screen = screen
    def draw_node(self,todel):
        screen = self.screen
        if todel:
            pygame.draw.circle(screen, (230, 230, 230), self.to_int(), self.radius, 0)
        else:
            pygame.draw.circle(screen, (96, 96, 96), self.to_int(), self.radius, 0)
        return 
    def draw_obnode(self):
        screen = self.screen
        pygame.draw.circle(screen, (30, 170, 30), self.to_int(), self.radius, 0)
        return
    def change_pos(self,newpos):
        self.pos = newpos
        return 
    def clicked(self,mouse_pos):
        distance = ((self.pos.x-mouse_pos[0])**2+(self.pos.y-mouse_pos[1])**2)**0.5
        if distance <= self.radius+10:
            return True
        else:
            return False
    def to_int(self):
        return int(self.pos.x), int(self.pos.y)
    def damaged(self,force_ext):
        return self.maxforce < abs(force_ext)
    def displacing(self,force_ext):
        return self.maxforce < abs(force_ext)
