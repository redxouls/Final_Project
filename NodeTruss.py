import sys, pygame
import numpy as np
from pygame.locals import *
from vpython import *
import ball

class Node :
    def __init__(self,x=0,y =0,screen=None,*,pos=None,radius=None):
        if pos == None:
            self.pos = vector(x,y,0)
        else:
            self.pos = pos
        self.radius = 10
        self.maxforce = 100
        self.screen = screen
    def draw_node(self):
        screen = self.screen
        pygame.draw.circle(screen, (0, 127, 255), self.to_int(), self.radius, 0)
        return 
    def change_pos(self,newpos):
        self.pos = newpos
        return 
    def clicked(self,mouse_pos):
        distance = ((self.pos.x-mouse_pos[0])**2+(self.pos.y-mouse_pos[1])**2)**0.5
        if distance <= self.radius:
            return True
        else:
            return False
    def to_int(self):
        return int(self.pos.x), int(self.pos.y)
    def damaged(self,force_ext):
        return self.maxforce < abs(force_ext)

class Truss(Node):
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
        
    def draw_Truss(self):
        screen = self.screen
        pygame.draw.line(self.screen,(0,0,0), self.nodeA.to_int(), self.nodeB.to_int(), 5)

    def draw_marked_Truss(self):
        screen = self.screen
        pygame.draw.line(self.screen,(0,200,0), self.nodeA.to_int(), self.nodeB.to_int(), 5) 

    def damaged(self,force_ext):
        return self.maxforce>force_ext
    
    def length(self):
        return mag(self.nodeA.pos-self.nodeB.pos)

class Bio():
    def __init__(self,*,pos=None, axis=None,screen=None,d=2.5*20,nodeA=None,nodeB=None):
        if nodeA != None and nodeB!= None: 
            self.O = nodeA
            self.C = nodeB
            axis = nodeA.pos-nodeB.pos
            d = axis.mag
        else:
            self.O = Node(pos=pos, radius=20)
            self.C = Node(pos=pos+axis, radius=20)
        self.bond = Truss(pos=pos, axis=axis, radius=20/2.0)
        self.O.m = 20
        self.C.m = 20
        self.O.v = vector(0, 0, 0)
        self.C.v = vector(0, 0, 0)
        self.d = d
        self.dt = 0.1
        self.bond.k = 500.0
        self.screen = screen
        self.b =  0.05 * sqrt(self.bond.k*self.O.m)
        self.gravity = vector(0,9.8,0)
    def bond_force_on_O(self):        # return bond force acted on the O atom
        return self.bond.k * (mag(self.bond.axis)-self.d) * norm(self.bond.axis) - self.b*(self.O.v-(self.O.v+self.C.v)/2)

    def time_lapse(self):         # by bond's force, calculate a, v and pos of C and O, and bond's pos and axis after dt 
        dt = self.dt
        self.C.a = -self.bond_force_on_O() / self.C.m +  self.gravity  # 
        self.O.a = self.bond_force_on_O() / self.O.m + self.gravity # 
        '''
        if self.C.a.mag>200 or self.O.a.mag>200:
            print(self.C.a.mag,self.O.a.mag)
            self.C.a = vector(0,0,0)
            self.O.a = vector(0,0,0)
        '''
        self.C.v += self.C.a * dt
        self.O.v += self.O.a * dt
        self.C.pos += self.C.v * dt
        self.O.pos += self.O.v * dt
        self.bond.axis = self.C.pos - self.O.pos
        self.bond.pos = self.O.pos

    def ground_collision(self):
        if self.O.pos.y > 900:
            self.O.v.y*= -1
        if self.C.pos.y > 900:
            self.C.v.y*= -1

    def collision(a1, a2):
        v1prime = a1.v - 2 * a2.m/(a1.m+a2.m) *(a1.pos-a2.pos) * dot (a1.v-a2.v, a1.pos-a2.pos) / mag(a1.pos-a2.pos)**2
        v2prime = a2.v - 2 * a1.m/(a1.m+a2.m) *(a2.pos-a1.pos) * dot (a2.v-a1.v, a2.pos-a1.pos) / mag(a2.pos-a1.pos)**2
        return v1prime, v2prime
    def system_check_collision(self,COs):
        N = len(COs)
        for i in range(N-1):        
            for j in range(i+1,N):  
                if (COs[i].C.pos-COs[j].C.pos).mag<=2*COs[i].C.radius and dot(COs[i].C.pos-COs[j].C.pos,COs[i].C.v-COs[j].C.v)<0:
                    COs[i].C.v, COs[j].C.v = Bio.collision(COs[i].C,COs[j].C)
                if (COs[i].C.pos-COs[j].O.pos).mag<=2*COs[i].C.radius and dot(COs[i].C.pos-COs[j].O.pos,COs[i].C.v-COs[j].O.v)<0:
                    COs[i].C.v, COs[j].O.v = Bio.collision(COs[i].C,COs[j].O)
                if (COs[i].O.pos-COs[j].C.pos).mag<=2*COs[i].C.radius and dot(COs[i].O.pos-COs[j].C.pos,COs[i].O.v-COs[j].C.v)<0:
                    COs[i].O.v, COs[j].C.v = Bio.collision(COs[i].O,COs[j].C)
                if (COs[i].O.pos-COs[j].O.pos).mag<=2*COs[i].C.radius and dot(COs[i].O.pos-COs[j].O.pos,COs[i].O.v-COs[j].O.v)<0:
                    COs[i].O.v, COs[j].O.v = Bio.collision(COs[i].O,COs[j].O)
    def draw_Truss(self,screen):
        pygame.draw.line(screen,(0,0,0), self.to_int(1), self.to_int(2), 8)
    def draw_node(self,screen):
        pygame.draw.circle(screen, (0, 127, 255), [int(self.O.pos.x), int(self.O.pos.y)], self.C.radius, 0)
        pygame.draw.circle(screen, (0, 127, 255), [int(self.C.pos.x), int(self.C.pos.y)], self.C.radius, 0)
        return
    def to_int(self, num):
        if num ==1:
            return [int(self.C.pos.x),int(self.C.pos.y)] 
        if num ==2:
            return [int(self.O.pos.x),int(self.O.pos.y)]
    def add_link(self,nodeA,nodeB):
        return Bio(nodeA=nodeA,nodeB=nodeB)

