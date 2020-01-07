import sys, pygame, time, copy
import numpy as np
from pygame.locals import *
from anastruct import SystemElements
from vpython import *
from Ball import *
from Node import *
from Truss import *
from Bio import *

class Structure:
    def __init__(self,screen):
        self.truss_limit = 20
        self.trusses = []
        self.nodes = []
        self.click = False
        self.lastc = 0
        self.screen = screen
        self.t = 0
        self.Bios = []
        self.loadid = None
        self.roadtrusses=[]
        self.collapse = False
        self.dlt=False
        self.dltcod=[(0,0),(0,0)]
        self.dltnode=[]
        self.dlttruss=[]
        self.tmpc=[False,(0,0),120]
        self.unstable = False
        self.tempnodespos = []
    def add(self,newtruss=None,newnode=None):
        if newtruss!= None:
            self.trusses.append(newtruss)
        if newnode!= None:
            self.trusses.append(newnode)
    
    def add_node(self,x,y):
        if len(self.trusses)> self.truss_limit +1 :
            return
        new_node = Node(x=int(x),y=int(y),screen=self.screen)
        self.nodes.append(new_node)
        return new_node
    
    def add_truss(self,nodeA,nodeB,mode):
        if len(self.trusses) > self.truss_limit+1 :
            return
        new_truss = Truss(nodeA,nodeB,self.screen)
        self.trusses.append(new_truss)
        if mode==0:
            self.roadtrusses.append(new_truss)
        print(self.Bios)
        return new_truss

    def print_result(self):
        nodes = self.nodes
        trusses = self.trusses
        for i in range(len(nodes)):
            print('nodes: ',i,nodes[i].pos)
        for i in range(len(trusses)):
            print('lines: ',i,trusses[i].nodeA.pos,'linkto',trusses[i].nodeB.pos)

    def two_end(self):
        if len(self.nodes)>0:
            left, right = self.nodes[0].pos,self.nodes[0].pos
            leftid, rightid = 0, 0
            for i in range(len(self.nodes)):
                node = self.nodes[i]
                if node.pos.x <left.x:
                    left = node.pos
                    leftid = i
                else:
                    if node.pos.x == left.x and node.pos.y>left.y:
                        left = node.pos
                        leftid = i
                if node.pos.x >right.x:
                    right = node.pos
                    rightid = i
                else:
                    if node.pos.x == right.x and node.pos.y>right.y:
                        right = node.pos
                        rightid = i
            return leftid,rightid
    
    def analyze(self):
        try:
            if len(self.nodes)<1:
                return None
            nodes = self.nodes
            trusses = self.trusses
            ss = SystemElements(EA=15000, EI=5000)
            for i in trusses:
                ta=[i.nodeA.pos.x,i.nodeA.pos.y]
                tb=[i.nodeB.pos.x,i.nodeB.pos.y]
                ss.add_element(location=[ta,tb])
            ends = self.two_end()
            ss.add_support_hinged(1)
            ss.add_support_hinged(2)
            ss.add_support_hinged(3)
            ss.add_support_hinged(4)
            #ss.add_support_roll(1,2)
            #ss.add_support_roll(1,2)
            if self.loadid != None:
                print(self.loadid)
                for i in self.loadid:
                    ss.point_load(i+1,Fy=30)
                    #ss.show_structure()
                
            else:
                return
            ss.solve()
            #ss.show_structure()
            #ss.show_axial_force()
            #ss.show_displacement()
            dispalcements = ss.get_node_displacements()
            for k in range(len(nodes)):
                newpos = vector(nodes[k].pos.x+dispalcements[k][1]*0.1,nodes[k].pos.y+dispalcements[k][2]*0.1,0)
                nodes[k].change_pos(newpos)

            self.t+=0.1
            return "success"
        except:
            self.unstable = True
            self.collapse = True
