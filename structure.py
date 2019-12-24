import sys, pygame, time
import numpy as np
from pygame.locals import *
import NodeTruss, ball
from anastruct import SystemElements
from vpython import *

Node = NodeTruss.Node
Truss = NodeTruss.Truss
Ball = ball.Ball
class Structure:
    def __init__(self,screen):
        self.trusses = []
        self.nodes = []
        self.click = False
        self.lastc = 0
        self.screen = screen
        self.t = 0
        self.balls = []
        self.collision=0
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
        return new_truss
    
    def add_ball(self):
        new_ball = Ball(self.screen)
        self.balls.append(new_ball)

    def length(self,choice):
        if choice == 'nodes':
            return len(self.nodes)
        if choice == 'trusses':
            return len(self.trusses)
    
    def print_result(self):
        nodes = self.nodes
        trusses = self.trusses
        for i in range(len(nodes)):
            print('nodes: ',i,nodes[i].cod)
        for i in range(len(trusses)):
            print('lines: ',i,trusses[i].nodeA.cod,'linkto',trusses[i].nodeB.cod)
    
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
        print(xlist,ylist)        
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
            left, right = self.nodes[0].cod,self.nodes[0].cod
            leftid, rightid = 0, 0
            for i in range(len(self.nodes)):
                node = self.nodes[i]
                if node.cod[0] <left[0]:
                    left = node.cod
                    leftid = i
                else:
                    if node.cod[0] == left[0] and node.cod[1]>left[1]:
                        left = node.cod
                        leftid = i
                if node.cod[0] >right[0]:
                    right = node.cod
                    rightid = i
                else:
                    if node.cod[0] == right[0] and node.cod[1]>right[1]:
                        right = node.cod
                        rightid = i
            return leftid,rightid
    
    def analyze(self):
        if len(self.nodes)<1:
            return None
        nodes = self.nodes
        trusses = self.trusses
        ss = SystemElements(EA=15000, EI=5000)
        for i in trusses:
            ta=[i.nodeA.cod[0],i.nodeA.cod[1]]
            tb=[i.nodeB.cod[0],i.nodeB.cod[1]]
            ss.add_element(location=[ta,tb])
        ends = self.two_end()
        ss.add_support_hinged(ends[0]+1)
        ss.add_support_hinged(ends[1]+1)
        #ss.add_support_roll(1,2)
        #ss.add_support_roll(1,2)
        self.loadid = 3+int(self.t)*2
        ss.point_load(self.loadid,Fy=50)
        ss.solve()
        #ss.show_structure()
        ss.show_axial_force()
        #ss.show_displacement()
        dispalcements = ss.get_node_displacements()
        forces = ss.get_node_results_system()
        axial_forces = ss.get_element_result_range('axial')
        #print([(round(i[0],3),round(i[2],3)) for i in forces])
        #print([round(i,3) for i in axial_forces])
        discon = []
        for i in range(len(axial_forces)):
            force = axial_forces[i]
            tpoint = nodes.index(trusses[i].nodeA), nodes.index(trusses[i].nodeB)
            if nodes[tpoint[0]].damaged(force) or nodes[tpoint[1]].damaged(force):
                discon.append((i,nodes[tpoint[0]].damaged(force),nodes[tpoint[1]].damaged(force)))
        print(discon)

        for k in range(len(nodes)):
            newcod = [nodes[k].cod[0]+dispalcements[k][3],nodes[k].cod[1]+dispalcements[k][2]*0.1]
            nodes[k].change_cod(newcod)

        self.t+=0.1
        return "success"
    
    def ball_rolling(self):
        dt = 0.1
        self.t += dt
        for ball in self.balls:
            if ball.ground_distance(self)!= None:
                if ball.ground_distance(self)-ball.r < 0.001 :
                    self.collision = self.t
                    print('gg',ball.v.mag,self.t)
                    ball.collision(self)
                    ball.a = vector(0,ball.g,0)+ball.engine(self)-ball.normala(self)
                else:
                    ball.a = vector(0,ball.g,0)+ ball.v*ball.efficient
                if ball.ground_distance(self)-ball.r < 1:
                    ball.a = vector(0,ball.g,0)+ball.engine(self)-ball.normala(self)
            else:
                ball.a = vector(0,ball.g,0)+ ball.v*ball.efficient
                    
                       
            ball.v += ball.a*dt
            ball.pos += ball.v*dt
              
            

    def update(self):
        screen = self.screen
        #self.analyze()
        self.screen.fill((255,255,255))    
        if self.balls != None:
            self.ball_rolling()    
        for i in self.nodes:
            i.draw_node()
        for i in self.trusses:
            i.draw_Truss()
        for i in self.balls:
            i.draw_ball()
        #time.sleep(0.1)