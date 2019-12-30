import sys, pygame, time, copy
import numpy as np
from pygame.locals import *
from anastruct import SystemElements
from vpython import *
from ball import *
from Node import *
from Truss import *
from Bio import *
from anastruct.basic import FEMException


class Structure:
    def __init__(self,screen):
        self.trusses = []
        self.nodes = []
        self.click = False
        self.lastc = 0
        self.screen = screen
        self.t = 0
        self.balls = []
        self.Bios = []
        self.loadid = None
        self.roadtrusses=[]
        self.mode=0
        self.running = False
        self.reset = False
        self.first = False
        self.collapse = False
    
    def add(self,newtruss=None,newnode=None):
        if newtruss!= None:
            self.trusses.append(newtruss)
        if newnode!= None:
            self.trusses.append(newnode)
    
    def add_node(self,x,y):
        new_node = Node(x=int(x),y=int(y),screen=self.screen)
        self.nodes.append(new_node)
        return new_node
    
    def add_truss(self,nodeA,nodeB):
        new_truss = Truss(nodeA,nodeB,self.screen)
        self.trusses.append(new_truss)
        if self.mode==0:
            self.roadtrusses.append(new_truss)
        #self.Bios.append(NodeTruss.Bio(nodeA=nodeA,nodeB=nodeB,screen=self.screen))
        print(self.Bios)
        return new_truss
    
    def add_ball(self):
        new_ball = Ball(self.screen)
        self.balls.append(new_ball)

    def print_result(self):
        nodes = self.nodes
        trusses = self.trusses
        for i in range(len(nodes)):
            print('nodes: ',i,nodes[i].pos)
        for i in range(len(trusses)):
            print('lines: ',i,trusses[i].nodeA.pos,'linkto',trusses[i].nodeB.pos)
    
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
                cur = self.add_node(xlist[i],ylist[i]-80)
            else:
                prev=cur
                cur = self.add_node(xlist[i],ylist[i])
            if cur != None and prev != None:
                pass
                self.add_truss(prev,cur)
        '''
        for i in range(1,len(xlist)-2,2):
            self.add_truss(self.nodes[i],self.nodes[i+2])
        for i in range(0,len(xlist)-2,2):
            self.add_truss(self.nodes[i],self.nodes[i+2])    
        '''
    
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
            newpos = vector(nodes[k].pos.x+dispalcements[k][1],nodes[k].pos.y+dispalcements[k][2],0)
            nodes[k].change_pos(newpos)

        self.t+=0.1
        return "success"
    
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
    
    def structure_save(self):
        self.tempnodespos =[0]*len(self.nodes) 
        for i in range(len(self.nodes)):
            self.tempnodespos[i] = self.nodes[i].pos

    def structure_reset(self):
        for i in range(len(self.tempnodespos)):
            self.nodes[i].pos = self.tempnodespos[i]
    
    def check_collapse(self):
        for truss in self.trusses:
            if truss.length()>truss.oril+3:
                print("collapse")
                self.running = False
                self.collapse = True
                truss.collapse = True
                self.Bios.append(Bio(nodeA=Node(pos=truss.nodeA.pos),nodeB=(Node(pos=truss.nodeB.pos))))
    
    def initail_platform(self):
        left_nodeA = self.add_node(0,480)
        left_nodeB = self.add_node(200,480)
        self.add_truss(left_nodeA,left_nodeB)
        right_nodeA = self.add_node(1080,480)
        right_nodeB = self.add_node(1280,480)
        self.add_truss(right_nodeA,right_nodeB)

    def update(self):
        screen = self.screen
        if self.running:
            self.check_collapse()
            if not self.collapse:
                self.analyze()
                time.sleep(0.01)
        self.screen.fill((255,255,255))    
        if self.balls != None:
            self.ball_rolling()    
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