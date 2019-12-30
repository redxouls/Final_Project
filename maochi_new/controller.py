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
class Controller():
    def __init__(self,structures_list):
        self.sturct_list = structures_list
    def clicked(self,event_type,mouse_pos,event_button):
        screen,nodes,click,trusses = self.struc_list[0].screen, self.struc_list[0].nodes, self.struc_list[0].click, self.struc_list[0].trusses
        downcod , upcod = mouse_pos, mouse_pos
        for i in range(len(nodes)):
            check = nodes[i]
            if check.clicked(mouse_pos):
                if event_type == MOUSEBUTTONDOWN:
                    self.struc_list[0].lastc = i
                    self.struc_list[0].click = True
                    return
                if event_type == MOUSEBUTTONUP and self.struc_list[0].click:
                    if nodes[self.struc_list[0].lastc].clicked(mouse_pos):            
                        self.struc_list[0].click = False
                        return
                    else:
                        self.struc_list[0].add_truss(nodes[self.struc_list[0].lastc],nodes[i])
                        self.struc_list[0].click = False
                        return
                return
        self.struc_list[0].add_node(mouse_pos[0],mouse_pos[1])
        lastc = len(nodes)-1
        if event_button == 3 and not self.struc_list[0].click:
            print("r")
            self.struc_list[0].click = True
            self.struc_list[0].lastc = len(nodes)-1
        if event_type == MOUSEBUTTONUP and self.struc_list[0].click:
            self.struc_list[0].add_truss(nodes[self.struc_list[0].lastc],nodes[-1])
            self.struc_list[0].click = False
            return
    '''
    create內容未改
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
        
        for i in range(1,len(xlist)-2,2):
            super(Controller,self).add_truss(self.nodes[i],self.nodes[i+2])
        for i in range(0,len(xlist)-2,2):
            super(Controller,self).add_truss(self.nodes[i],self.nodes[i+2])    
        
        '''
    def update(self):
        screen =self.struc_list[0].screen
        if self.struc_list[0].running:
            self.struc_list[0].check_collapse() ############check_collapse
            if not self.struc_list[0].collapse:
                self.struc_list[0].analyze()
                time.sleep(0.01)
        self.struc_list[0].screen.fill((255,255,255))    
        if self.struc_list[0].balls != None:
            self.struc_list[0].ball_rolling()  #########3   
        for i in self.struc_list[0].nodes:
            i.draw_node()
        for i in self.struc_list[0].trusses:
            if i.collided and not i.collapse :
                i.draw_marked_Truss()
            else:
                if not i.collapse:
                    i.draw_Truss()
        for i in self.struc_list[0].balls:
            i.draw_ball()
            ########################boll_rolling的self不太確定
    def ball_rolling(self):
            dt = 0.1
            self.struc_list[0].t += dt
            for ball in self.struc_list[0].balls:
                if ball.ground_distance(self)!= None:
                    if ball.ground_distance(self)-ball.radius < 0.001 :
                        self.collision = self.struc_list[0].t
                        ball.collision(self)
                        ball.a = vector(0,ball.g,0)+ball.engine(self)-ball.normala(self)
                    else:
                        self.struc_list[0].loadid = None
                        ball.a = vector(0,ball.g,0)+ ball.v*ball.efficient
                    
                    if ball.ground_distance(self)-ball.radius < 0.01:
                        ball.a = vector(0,ball.g,0)+ball.engine(self)-ball.normala(self)
                    
                else:
                    ball.a = vector(0,ball.g,0)+ ball.v*ball.efficient

                ball.v += ball.a*dt
                ball.pos += ball.v*dt
    def initail_platform(self):
        left_nodeA = self.struc_list[0].add_node(0,480)
        left_nodeB = self.struc_list[0].add_node(200,480)
        self.struc_list[0].add_truss(left_nodeA,left_nodeB)
        right_nodeA = self.struc_list[0].add_node(1080,480)
        right_nodeB = self.struc_list[0].add_node(1280,480)
        self.struc_list[0].add_truss(right_nodeA,right_nodeB)

