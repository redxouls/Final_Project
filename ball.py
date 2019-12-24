import sys, pygame, time
import numpy as np
from pygame.locals import *
import NodeTruss, structure
from anastruct import SystemElements
from vpython import *


class Ball:
    def __init__(self,screen):
        self.screen = screen
        self.r = 20
        self.g = 9.8
        self.efficient = -0.2
        self.power = 70.0
        self.v = vector(0,0,0)
        self.pos = vector(120.0,100.0,0)
        self.a = vector(0,self.g,0)
        self.free = True
    def distance(self,*,node=None,truss=None):
        if node != None:
            return (self.pos[0]-node.cod[0]**2+(self.pos[1]-node.cod[1]**2)**0.5)
        if truss != None:
            return 
    def draw_ball(self):
        screen = self.screen
        pygame.draw.circle(screen, (123, 127, 255), [int(self.pos.x),int(self.pos.y)], self.r, 0)
    def nearest(self,structure):
        for i in range(len(structure.trusses)):
            truss = structure.trusses[i] 
            if self.pos.x>=truss.nodeA.x and self.pos.x<truss.nodeB.x:
                return i
            if self.pos.x<truss.nodeA.x and self.pos.x>=truss.nodeB.x:
                return i
    def ground_distance(self,structure):
        if self.nearest(structure) == None:
            return
        ground = structure.trusses[self.nearest(structure)]
        v1 = self.pos - vector(ground.nodeA.x,ground.nodeA.y,0)
        v2 = vector(ground.nodeB.x,ground.nodeB.y,0) - vector(ground.nodeA.x,ground.nodeA.y,0)
        theta = acos(v1.dot(v2)/(v1.mag*v2.mag))
        distance = v1.mag*sin(theta)
        return distance
    def collision(self,structure):
        if self.nearest(structure) == None:
            return
        ground = structure.trusses[self.nearest(structure)]
        v1 = self.pos - vector(ground.nodeA.x,ground.nodeA.y,0)
        v2 = vector(ground.nodeB.x,ground.nodeB.y,0) - vector(ground.nodeA.x,ground.nodeA.y,0)
        v2 /= v2.mag
        N = vector(-v2.y,v2.x,0)
        if N.dot(self.v)<=0:
            return
        newv = -self.v.dot(N)*N + self.v.dot(v2)*v2
        self.v = newv
    
    def engine(self,structure):
        if self.nearest(structure) == None:
            return
        ground = structure.trusses[self.nearest(structure)]
        v1 = self.pos - vector(ground.nodeA.x,ground.nodeA.y,0)
        v2 = vector(ground.nodeB.x,ground.nodeB.y,0) - vector(ground.nodeA.x,ground.nodeA.y,0)
        v2 /= v2.mag
        if v2.x<0:
            v2*=-1
        return self.power*v2
    
    def normala(self,structure):
        if self.nearest(structure) == None:
            return
        ground = structure.trusses[self.nearest(structure)]
        v1 = self.pos - vector(ground.nodeA.x,ground.nodeA.y,0)
        v2 = vector(ground.nodeB.x,ground.nodeB.y,0) - vector(ground.nodeA.x,ground.nodeA.y,0)
        v2 /= v2.mag
        N = vector(-v2.y,v2.x,0)
        return N.dot(vector(0,self.g,0))*N
    
    def fly(self,structure):
        if self.nearest(structure) == None:
            return False
        ground = structure.trusses[self.nearest(structure)]
        #or abs(self.pos.x-ground.nodeB.x)<5
        if abs(self.pos.x-ground.nodeA.x)<5 :
            return True
        else:
            return False
    