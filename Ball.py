import sys, pygame, time, os
import numpy as np
from pygame.locals import *
from anastruct import SystemElements
from vpython import *
from Node import *
from Truss import *

class Ball:
    def __init__(self,screen,label,pos=vector(0,0,0)):
        self.label = label
        self.screen = screen
        self.radius = 10
        self.g = 9.8
        self.efficient = 0.01
        self.colleffi = 0.8
        self.power = 40.0
        self.v = vector(0,0,0)
        self.pos = pos
        self.a = vector(0,self.g,0)
        self.free = True
    def distance(self,*,node=None,truss=None):
        if node != None:
            return (self.pos[0]-node.cod[0]**2+(self.pos[1]-node.cod[1]**2)**0.5)
        if truss != None:
            return 
    def draw_ball(self):
        screen = self.screen
        pygame.draw.circle(screen, (123, 127, 255), [int(self.pos.x),int(self.pos.y)], self.radius, 0)
    def nearest(self,structure):
        for i in range(len(structure.roadtrusses)):
            truss = structure.roadtrusses[i] 
            if truss.collapse:
                continue
            if self.pos.x>=truss.nodeA.pos.x and self.pos.x<truss.nodeB.pos.x:
                return i
            if self.pos.x<truss.nodeA.pos.x and self.pos.x>=truss.nodeB.pos.x:
                return i
    def ground_distance(self,structure):
        if self.nearest(structure) == None:
            return
        ground = structure.roadtrusses[self.nearest(structure)]
        v1 = self.pos - vector(ground.nodeA.pos.x,ground.nodeA.pos.y,0)
        v2 = vector(ground.nodeB.pos.x,ground.nodeB.pos.y,0) - vector(ground.nodeA.pos.x,ground.nodeA.pos.y,0)
        theta = acos(v1.dot(v2)/(v1.mag*v2.mag))
        distance = v1.mag*sin(theta)
        return distance

    def collision(self,structure,controller):
        if self.nearest(structure) == None:
            return
        ground = structure.roadtrusses[self.nearest(structure)]
        if ground.nodeA.pos.x<=ground.nodeA.pos.x:
            v1 = self.pos-vector(ground.nodeA.pos.x,ground.nodeA.pos.y,0)
            v2 = vector(ground.nodeB.pos.x,ground.nodeB.pos.y,0) - vector(ground.nodeA.pos.x,ground.nodeA.pos.y,0)
            v2 /= v2.mag
        else:
            v1 = self.pos-vector(ground.nodeA.pos.x,ground.nodeB.pos.y,0)
            v2 = vector(ground.nodeA.pos.x,ground.nodeA.pos.y,0) - vector(ground.nodeB.pos.x,ground.nodeB.pos.y,0)
            v2 /= v2.mag
        N = vector(v2.y,-v2.x,0)
        if (N.dot(self.v)<0 and v1.dot(N)>0) or (N.dot(self.v)>0 and v1.dot(N)<0):
            newv = -self.v.dot(N)*N*self.colleffi + self.v.dot(v2)*v2
            self.v = newv
            #structure.loadid[self.label] = [structure.nodes.index(structure.trusses[self.nearest(structure)].nodeA),structure.nodes.index(structure.trusses[self.nearest(structure)].nodeB)]
            print(asin(abs(v2.y))/pi*180)
            path8 = os.path.join(controller.dir,'car.png')
            controller.origin_car = pygame.image.load(path8).convert_alpha()
            controller.car_size = (80,60)
            controller.car = pygame.transform.scale(controller.origin_car,controller.car_size)
            controller.car = pygame.transform.rotate(controller.car,asin(abs(v2.y))/pi*180)
        else:
            return
    
    def engine(self,structure):
        if self.nearest(structure) == None:
            return
        ground = structure.roadtrusses[self.nearest(structure)]
        v1 = self.pos - vector(ground.nodeA.pos.x,ground.nodeA.pos.y,0)
        v2 = vector(ground.nodeB.pos.x,ground.nodeB.pos.y,0) - vector(ground.nodeA.pos.x,ground.nodeA.pos.y,0)
        v2 /= v2.mag
        v1 /= v1.mag
        if v2.x<0:
            v2*=-1
        structure.loadid[self.label] = [structure.nodes.index(structure.trusses[self.nearest(structure)].nodeA),structure.nodes.index(structure.trusses[self.nearest(structure)].nodeB)]
        ground.collided = True
        return self.power*v2-v1

    def normala(self,structure):
        if self.nearest(structure) == None:
            return
        ground = structure.roadtrusses[self.nearest(structure)]
        v1 = self.pos - vector(ground.nodeA.pos.x,ground.nodeA.pos.y,0)
        v2 = vector(ground.nodeB.pos.x,ground.nodeB.pos.y,0) - vector(ground.nodeA.pos.x,ground.nodeA.pos.y,0)
        v2 /= v2.mag
        N = vector(-v2.y,v2.x,0)
        return N.dot(vector(0,self.g,0))*N
    