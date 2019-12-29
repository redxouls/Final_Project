import sys, pygame, time, copy
import numpy as np
from pygame.locals import *
from anastruct import SystemElements
from vpython import *
from ball import *
from Node import *
from Truss import *
from Bio import *
from structure import *
class Controller(Structure):
    def __init__(self,screen,trusses,nodes,click,lastc,t,balls,Bios,loadid,roadtrusses,mode,running,reset,first,collapse):
        self.screen = screen
        self.trusses = trusses
        self.nodes = nodes
        self.click = click
        self.lastc = lastc
        self.t = t
        self.balls = balls
        self.Bios = Bios
        self.loadid = loadid
        self.roadtrusses= roadtrusses
        self.mode= mode
        self.running = running
        self.reset = reset
        self.first = first
        self.collapse = collapse
    def clicked(self,event_type,mouse_pos,event_button):
        screen,nodes,click,trusses = self.screen, self.nodes, self.click, self.trusses
        downcod , upcod = mouse_pos, mouse_pos
        for i in range(len(nodes)):
            check = nodes[i]
            if check.clicked(mouse_pos):
                if event_type == MOUSEBUTTONDOWN:
                    self.lastc = i
                    self.click = True
                    return
                if event_type == MOUSEBUTTONUP and self.click:
                    if nodes[self.lastc].clicked(mouse_pos):            
                        self.click = False
                        return
                    else:
                        self.add_truss(nodes[self.lastc],nodes[i])
                        self.click = False
                        return
                return
        self.add_node(mouse_pos[0],mouse_pos[1])
        lastc = len(nodes)-1
        if event_button == 3 and not self.click:
            print("r")
            self.click = True
            self.lastc = len(nodes)-1
        if event_type == MOUSEBUTTONUP and self.click:
            self.add_truss(nodes[self.lastc],nodes[-1])
            self.click = False
            return
    def create(self,xlist=0,ylist=0):
        screen = self.screen
        xlist = np.arange(1, 15) * np.pi
        ylist = np.cos(xlist)
        xlist = np.arange(1, 15) *4
        ylist -= ylist.min()    
        xlist*=20
        xlist-=50
        ylist*=10
        ylist+=300
        cur = None
        prev = None

        for i in range(len(xlist)):
            if i%2 ==1:
                prev=cur
                cur = super(Controller,self).add_node(xlist[i],ylist[i]-80)
            else:
                prev=cur
                cur = super(Controller,self).add_node(xlist[i],ylist[i])
            if cur != None and prev != None:
                pass
                super(Controller,self).add_truss(prev,cur)
        '''
        for i in range(1,len(xlist)-2,2):
            super(Controller,self).add_truss(self.nodes[i],self.nodes[i+2])
        for i in range(0,len(xlist)-2,2):
            super(Controller,self).add_truss(self.nodes[i],self.nodes[i+2])    
        '''
    def update(self):
        screen = self.screen
        if self.running:
            super(Controller,self).check_collapse() ############check_collapse
            if not self.collapse:
                self.analyze()
                time.sleep(0.01)
        self.screen.fill((255,255,255))    
        if self.balls != None:
            self.ball_rolling()  #########3   
        for i in self.nodes:
            i.draw_node()
        for i in self.trusses:
            if i.collided and not i.collapse :
                i.draw_marked_Truss()
            else:
                if not i.collapse:
                    i.draw_Truss()
        for i in self.balls:
            i.draw_ball()
    def ball_rolling(self):
            dt = 0.1
            self.t += dt
            for ball in self.balls:
                if ball.ground_distance(self)!= None:
                    if ball.ground_distance(self)-ball.radius < 0.001 :
                        self.collision = self.t
                        ball.collision(self)
                        ball.a = vector(0,ball.g,0)+ball.engine(self)-ball.normala(self)
                    else:
                        self.loadid = None
                        ball.a = vector(0,ball.g,0)+ ball.v*ball.efficient
                    
                    if ball.ground_distance(self)-ball.radius < 0.01:
                        ball.a = vector(0,ball.g,0)+ball.engine(self)-ball.normala(self)
                    
                else:
                    ball.a = vector(0,ball.g,0)+ ball.v*ball.efficient

                ball.v += ball.a*dt
                ball.pos += ball.v*dt
    def initail_platform(self):
        left_nodeA = super(Controller,self).add_node(0,480)
        left_nodeB = super(Controller,self).add_node(200,480)
        super(Controller,self).add_truss(left_nodeA,left_nodeB)
        right_nodeA = super(Controller,self).add_node(1080,480)
        right_nodeB = super(Controller,self).add_node(1280,480)
        super(Controller,self).add_truss(right_nodeA,right_nodeB)

