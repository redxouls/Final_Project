import sys, pygame
import numpy as np
from pygame.locals import *
import NodeTruss
Node = NodeTruss.Node
Truss = NodeTruss.Truss
class Structure:
    def __init__(self,screen):
        self.trusses = []
        self.nodes = []
        self.codtrusses=[]
        self.codnodes = []
        self.click = [False,0]
        self.screen = screen
    
    def add(self,newtruss=None,newnode=None):
        if newtruss!= None:
            self.trusses.append(newtruss)
        if newnode!= None:
            self.trusses.append(newnode)
    
    def add_node(self,x,y):
        new_node = Node(x=int(x),y=int(y),screen=self.screen)
        self.nodes.append(new_node)
        self.codnodes.append(new_node.cod)
        return new_node
    
    def add_truss(self,nodeA,nodeB):
        new_truss = Truss(nodeA,nodeB,self.screen)
        self.trusses.append(new_truss)
        self.codtrusses.append((new_truss.nodeA.cod,new_truss.nodeB.cod))
        return new_truss
    
    def length(self,choice):
        if choice == 'nodes':
            return len(self.nodes)
        if choice == 'lines':
            return len(self.trusses)
    
    def print_result(self):
        nodes = self.codnodes
        trusses = self.codtrusses
        for i in range(len(nodes)):
            print('nodes: ',i,nodes[i])
        for i in range(len(trusses)):
            print('lines: ',i,trusses[i][0],'linkto',trusses[i][1])
    
    def clicked(self,event_type,mouse_pos):
        screen = self.screen
        nodes = self.nodes
        click = self.click
        trusses = self.trusses
        downcod , upcod = mouse_pos, mouse_pos
        if event_type == MOUSEBUTTONDOWN:
            for i in range(len(nodes)):
                checkdown = nodes[i]
                self.click[0] = checkdown.clicked(downcod)
                if self.click[0]:
                    self.click[0],self.click[1] = True , i
                    break
            if not click[0]:
                nodes.append(Node(x =downcod[0],y=downcod[1],screen=screen))
        if event_type == MOUSEBUTTONUP:
            upclick = False
            for i in range(len(nodes)):
                check = nodes[i]
                if check.clicked(upcod):
                    trusses.append(Truss(nodes[i],nodes[click[1]],screen=screen))
                    trusses[-1].draw_Truss()
                    upclick = True
                    break
            if not upclick:
                nodes.append(Node(x=upcod[0],y=upcod[1],screen=screen))
                trusses.append(Truss(nodes[-1],nodes[click[1]],screen=screen))
                trusses[-1].draw_Truss()
    
    def create(self,xlist=0,ylist=0):
        screen = self.screen
        xlist = np.arange(1, 10) * np.pi
        ylist = np.cos(xlist)
        ylist -= ylist.min()            
        xlist*=20
        ylist*=20
        ylist+=100
        print(xlist,ylist)     
        cur = None
        prev = None
        for i in range(len(xlist)):
            if i%2 ==1:
                prev=cur
                cur = self.add_node(xlist[i],ylist[i]-80)
            else:
                prev=cur
                cur = self.add_node(xlist[i],ylist[i])
            if cur != None and prev != None:
                self.add_truss(prev,cur)
        
        for i in range(1,6,2):
            self.add_truss(self.nodes[i],self.nodes[i+2])
        for i in range(0,7,2):
            self.add_truss(self.nodes[i],self.nodes[i+2])    
    def two_end(self):
        if len(self.nodes)>0:
            left, right = self.nodes[0].cod,self.nodes[0].cod
            for i in range(len(self.nodes)):
                node = self.nodes[i]
                if node.cod[0] <left[0]:
                    left = node.cod
                else:
                    if node.cod[0] == left[0] and node.cod[1]>left[1]:
                        left = node.cod
                if node.cod[0] >right[0]:
                    right = node.cod
                else:
                    if node.cod[0] == right[0] and node.cod[1]>right[1]:
                        right = node.cod
        return left,right
    
    def update(self):
        for i in self.nodes:
            i.draw_node()
        for i in self.trusses:
            i.draw_Truss()



