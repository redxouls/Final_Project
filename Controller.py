import sys, pygame, time, copy
import numpy as np
from pygame.locals import *
from anastruct import SystemElements
from vpython import *
from Ball import *
from Node import *
from Truss import *
from Bio import *
from Structure import *

class Controller():
    def __init__(self,structure,screen):
        self.sturcture = structure
        self.screen = screen
        self.balls = []
        self.t = 0
        self.dlt=False
        self.dltcod=[(0,0),(0,0)]
        self.mode = 0
        self.running = False
        self.first = False
        self.Bios = []
    def add_ball(self):
        new_ball = Ball(self.screen)
        self.balls.append(new_ball)

    def clicked(self,event_type,mouse_pos,event_button):
        structure = self.sturcture
        screen,nodes,click,trusses = structure.screen, structure.nodes, structure.click, structure.trusses
        downcod , upcod = mouse_pos, mouse_pos
        for i in range(len(nodes)):
            check = nodes[i]
            if check.clicked(mouse_pos):
                if event_type == MOUSEBUTTONDOWN:
                    structure.lastc = i
                    structure.click = True
                    return
                if event_type == MOUSEBUTTONUP and structure.click:
                    if nodes[structure.lastc].clicked(mouse_pos):            
                        structure.click = False
                        return
                    else:
                        structure.add_truss(nodes[structure.lastc],nodes[i],self.mode)
                        structure.click = False
                        return
                return
        structure.add_node(mouse_pos[0],mouse_pos[1])
        lastc = len(nodes)-1
        if event_button == 3 and not structure.click:
            print("r")
            structure.click = True
            structure.lastc = len(nodes)-1
        if event_type == MOUSEBUTTONUP and structure.click:
            structure.add_truss(nodes[structure.lastc],nodes[-1],self.mode)
            structure.click = False
            return
        
    def ball_rolling(self):
        dt = 0.1
        structure = self.sturcture
        self.t += dt
        for ball in self.balls:
            if ball.ground_distance(structure)!= None:
                if ball.ground_distance(structure)-ball.radius < 0.001 :
                    structure.collision = self.t
                    ball.collision(structure)
                    ball.a = vector(0,ball.g,0)+ball.engine(structure)-ball.normala(structure)
                else:
                    structure.loadid = None
                    ball.a = vector(0,ball.g,0)+ ball.v*ball.efficient
                
                if ball.ground_distance(structure)-ball.radius < 0.01:
                    ball.a = vector(0,ball.g,0)+ball.engine(structure)-ball.normala(structure)
                
            else:
                ball.a = vector(0,ball.g,0)+ ball.v*ball.efficient

            ball.v += ball.a*dt
            ball.pos += ball.v*dt

    def structure_save(self):
        structure = self.sturcture
        structure.tempnodespos =[0]*len(structure.nodes) 
        for i in range(len(structure.nodes)):
            structure.tempnodespos[i] = structure.nodes[i].pos

    def structure_reset(self):
        structure = self.sturcture
        for i in range(len(structure.tempnodespos)):
            structure.nodes[i].pos = structure.tempnodespos[i]
    
    def check_collapse(self):
        structure = self.sturcture
        for truss in structure.trusses:
            if truss.length()>truss.oril+1:
                print("collapse")
                self.running = False
                structure.collapse = True
                truss.collapse = True
                nodeB = Node(pos=truss.oril*norm(truss.nodeB.pos-truss.nodeA.pos)+truss.nodeA.pos)
                self.Bios.append(Bio(nodeA=Node(pos=truss.nodeA.pos),nodeB=nodeB))
    
    def initail_platform(self):
        structure = self.sturcture
        left_nodeA = structure.add_node(0,480)
        left_nodeB = structure.add_node(200,480)
        structure.add_truss(left_nodeA,left_nodeB,0)
        right_nodeA = structure.add_node(1080,480)
        right_nodeB = structure.add_node(1280,480)
        structure.add_truss(right_nodeA,right_nodeB,0)

    def delarea(self):
        structure = self.sturcture
        x1=self.dltcod[0][0]
        x2=self.dltcod[1][0]
        y1=self.dltcod[0][1]
        y2=self.dltcod[1][1]
        dltnode=[]
        for nd in structure.nodes:
            if (nd.pos.x-x1)*(nd.pos.x-x2)<0 and (nd.pos.y-y1)*(nd.pos.y-y2)<0:
                dltnode.append(nd)
                #print(nd.pos)
        for nd in dltnode:
            for tru in structure.trusses:
                if tru.nodeA == nd or tru.nodeB == nd:
                    structure.trusses.remove(tru)
            structure.nodes.remove(nd)
        print(len(structure.trusses))
        dlttruss=[]
        for tru in structure.trusses:
            #print(tru.nodeB.pos,tru.nodeA.pos)
            xpara=(tru.nodeA.pos.x,tru.nodeB.pos.x-tru.nodeA.pos.x)
            ypara=(tru.nodeA.pos.y,tru.nodeB.pos.y-tru.nodeA.pos.y)
            #print(ypara)
            cnt=0
            if xpara[1] != 0:
                if (0<(x1-xpara[0])/xpara[1]<1 and min(y1,y2)<ypara[0]+(x1-xpara[0])/xpara[1]*ypara[1]<max(y1,y2)) or (0<(x2-xpara[0])/xpara[1]<1 and min(y1,y2)<ypara[0]+(x2-xpara[0])/xpara[1]*ypara[1]<max(y1,y2)): 
                    cnt+=1
            elif xpara[1] == 0:
                if min(x1,x2)<xpara[0]<max(x1,x2) and (0<(y1-ypara[0])/ypara[1]<1 or 0<(y2-ypara[0])/ypara[1]<1):
                    cnt+=1
            if ypara[1] != 0:
                if (0<(y1-ypara[0])/ypara[1]<1 and min(x1,x2)<xpara[0]+(y1-ypara[0])/ypara[1]*xpara[1]<max(x1,x2)) or (0<(y2-ypara[0])/ypara[1]<1 and min(x1,x2)<xpara[0]+(y2-ypara[0])/ypara[1]*xpara[1]<max(x1,x2)): 
                    cnt+=1
            elif ypara[1] == 0:
                if min(y1,y2)<ypara[0]<max(y1,y2) and (0<(x1-xpara[0])/xpara[1]<1 or 0<(x2-xpara[0])/xpara[1]<1):
                    cnt+=1
            if cnt >= 1:
                dlttruss.append(tru)
        for tru in dlttruss:
            structure.trusses.remove(tru)

    def update(self):
        structure = self.sturcture
        screen = self.screen
        if self.running:
            self.check_collapse()
            if not structure.collapse:
                structure.analyze()
                time.sleep(0.01)
        structure.screen.fill((255,255,255))    
        if self.balls != None:
            self.ball_rolling()    
        for i in structure.nodes:
            i.draw_node()
        for i in structure.trusses:
            if i in structure.roadtrusses :
                if not i.collapse:
                    i.draw_marked_Truss()
            else:
                if not i.collapse:
                    i.draw_Truss()
        for i in self.balls:
            i.draw_ball()
