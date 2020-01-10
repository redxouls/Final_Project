import sys, pygame, time, copy, os
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
        self.win = False
        self.di = os.getcwd()
        self.dir = os.path.join(self.di,'images')
        path10 = os.path.join(self.dir,'esc_bg2.png')
        self.background_size = (1280,960)
        self.origin_game_bg = pygame.image.load(path10).convert_alpha()
        self.game_bg = pygame.transform.scale(self.origin_game_bg,self.background_size)
        #
        self.structure = structure
        self.screen = screen
        self.balls = []
        self.t = 0
       
        self.mode = 0
        self.running = False
        self.first = False
        self.Bios = []
        #
        self.game_running = False
        self.first_time = True
        self.first_click = True
        self.esc_or_not = False
        #
        self.lastc = 0
        self.click = False
        self.dlt=False
        self.dltcod=[(0,0),(0,0)]
        self.dltnode=[]
        self.dlttruss=[]
        self.tmpc=[False,(0,0),200]
        self.win = False
        self.altednode = -1
        self.alt = [False,False]
        self.reltruss=[]
        path8 = os.path.join(self.dir,'car.png')
        self.origin_car = pygame.image.load(path8).convert_alpha()
        self.car_size = (80,60)
        self.car = pygame.transform.scale(self.origin_car,self.car_size)
        self.display_mode = 'Road'
        self.mode_font = pygame.font.SysFont('Comic Sans MS', 35)
        self.running_mode = 'Stop'
        self.running_font = pygame.font.SysFont('Comic Sans MS', 35)
        self.fail_font = pygame.font.SysFont('Comic Sans MS', 80) 
        self.fail_textsurface = self.fail_font.render('You lose! Try Again!', False, (255, 0, 0))
        self.fail_rect = self.fail_textsurface.get_rect()
        self.limit_font = pygame.font.SysFont('Comic Sans MS',35)
    def add_ball(self):
        new_ball = Ball(self.screen)
        self.balls.append(new_ball)

    def clicked(self,event_type,mouse_pos,event_button):
        structure = self.structure
        screen,nodes,click,trusses = structure.screen, structure.nodes, self.click, structure.trusses
        downcod , upcod = mouse_pos, mouse_pos
        for i in range(len(nodes)):
            check = nodes[i]
            if check.clicked(mouse_pos):
                if event_type == MOUSEBUTTONDOWN:
                    self.lastc = i
                    self.click = True
                    self.tmpc[0]=True
                    self.tmpc[1]=(check.to_int())
                    return
                if event_type == MOUSEBUTTONUP and self.click:
                    if nodes[self.lastc].clicked(mouse_pos):            
                        self.click = False
                        return
                    else:
                        if (nodes[self.lastc].pos.x-structure.nodes[i].pos.x)**2+(nodes[self.lastc].pos.y-structure.nodes[i].pos.y)**2<=self.tmpc[2]**2:
                            structure.add_truss(nodes[self.lastc],nodes[i],self.mode)
                        self.click = False
                        return
                return
        structure.add_node(mouse_pos[0],mouse_pos[1])
        if event_type == MOUSEBUTTONDOWN:
            self.tmpc[0]=True
            self.tmpc[1]=(mouse_pos[0],mouse_pos[1])
        
            if event_button == 3 and not self.click:
                self.click = True
                self.lastc = len(nodes)-1
        #lastc = len(nodes)-1
        if event_type == MOUSEBUTTONUP and self.click:
            if (nodes[self.lastc].pos.x-structure.nodes[-1].pos.x)**2+(nodes[self.lastc].pos.y-structure.nodes[-1].pos.y)**2>self.tmpc[2]**2:
                structure.nodes.pop()
                self.lastc = 0
                self.click = False
                return
            structure.add_truss(nodes[self.lastc],nodes[-1],self.mode)
            self.click = False
            return
        
    def ball_rolling(self):
        dt = 0.1
        structure = self.structure
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
                
                if ball.ground_distance(structure)-ball.radius < 0.1:
                    ball.a = vector(0,ball.g,0)+ball.engine(structure)-ball.normala(structure)
                
            else:
                ball.a = vector(0,ball.g,0)+ ball.v*ball.efficient
            if ball.pos.x >= 1280 and ball.pos.y<700 and self.running:
                self.win = True
            ball.v += ball.a*dt
            ball.pos += ball.v*dt

    def structure_save(self):
        if self.structure.collapse:
            return
        structure = self.structure
        structure.tempnodespos =[0]*len(structure.nodes) 
        for i in range(len(structure.nodes)):
            structure.tempnodespos[i] = structure.nodes[i].pos

    def structure_reset(self):
        structure = self.structure
        if structure.tempnodespos == []:
            return
        structure.loadid = None
        structure.collapse = False
        self.balls  = []
        self.Bios = []
        for i in range(len(structure.tempnodespos)):
            structure.nodes[i].pos = structure.tempnodespos[i]
        for i in range(len(structure.trusses)):
            structure.trusses[i].collapse = False
    
    def check_collapse(self):
        structure = self.structure
        collpase = False
        for truss in structure.trusses:
            if truss.length()>truss.oril+1:
                collpase  = True
                self.running = True
                structure.collapse = True
                truss.collapse = True
                '''
                nodeB = Node(pos=truss.oril*norm(truss.nodeB.pos-truss.nodeA.pos)+truss.nodeA.pos)
                self.Bios.append(Bio(nodeA=Node(pos=truss.nodeA.pos),nodeB=nodeB))
                '''
        if collpase:
            for truss in structure.trusses:
                truss.collapse = True
                nodeB = Node(pos=truss.oril*norm(truss.nodeB.pos-truss.nodeA.pos)+truss.nodeA.pos)
                self.Bios.append(Bio(nodeA=Node(pos=truss.nodeA.pos),nodeB=nodeB))
                for truss in structure.roadtrusses:
                    truss.collapse = True

    def initial_platform(self):
        structure = self.structure
        left_nodeA = structure.add_node(0,700)
        left_nodeB = structure.add_node(200,700)
        structure.add_truss(left_nodeA,left_nodeB,0)
        right_nodeA = structure.add_node(1080,700)
        right_nodeB = structure.add_node(1280,700)
        structure.add_truss(right_nodeA,right_nodeB,0)

    def delarea(self):
        x1=self.dltcod[0][0]
        x2=self.dltcod[1][0]
        y1=self.dltcod[0][1]
        y2=self.dltcod[1][1]
        structure = self.structure
        for nd in structure.nodes:
            if structure.nodes.index(nd)<4:
                continue
            if (nd.pos.x-x1)*(nd.pos.x-x2)<0 and (nd.pos.y-y1)*(nd.pos.y-y2)<0:
                self.dltnode.append(nd)
        
        for tru in structure.trusses:
            if structure.trusses.index(tru)<2:
                continue
            xpara=(tru.nodeA.pos.x,tru.nodeB.pos.x-tru.nodeA.pos.x)
            ypara=(tru.nodeA.pos.y,tru.nodeB.pos.y-tru.nodeA.pos.y)
            cnt=0
            if min(x1,x2)<tru.nodeA.pos.x<max(x1,x2) and min(x1,x2)<tru.nodeB.pos.x<max(x1,x2) and min(y1,y2)<tru.nodeA.pos.y<max(y1,y2) and min(y1,y2)<tru.nodeB.pos.y<max(y1,y2):
                cnt+=1
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
                self.dlttruss.append(tru)
        
    def clear(self):
        structure = self.structure 
        for nd in self.dltnode:
            structure.nodes.remove(nd)
        for tru in self.dlttruss:
            structure.trusses.remove(tru)
            if tru in self.structure.roadtrusses:
                self.structure.roadtrusses.remove(tru)
        self.recov()

    def recov(self):
        self.dltnode=[]
        self.dlttruss=[]

    def update(self):
        structure  = self.structure
        if self.structure.unstable:
            for truss in structure.trusses:
                truss.collapse = True
                nodeB = Node(pos=truss.oril*norm(truss.nodeB.pos-truss.nodeA.pos)+truss.nodeA.pos)
                self.Bios.append(Bio(nodeA=Node(pos=truss.nodeA.pos),nodeB=nodeB))
                for truss in structure.roadtrusses:
                    truss.collapse = True
            self.structure.unstable = False
        structure = self.structure
        screen = self.screen
        if self.running and  not self.structure.collapse:
            self.check_collapse()
            if not structure.collapse:
                structure.analyze()
                time.sleep(0.01)
        #----------------------------------
        self.screen.blit(self.game_bg,(0,0))
        if self.mode == 0:
            self.display_mode = 'Road'
        elif self.mode == 1:
            self.display_mode = 'Wood'
        if self.running:
            self.running_mode = 'Running'
        else:
            self.running_mode = "Stop"
        self.mode_textsurface = self.mode_font.render('Mode = %s' %self.display_mode, False, (255, 255, 255))
        self.mode_rect = self.mode_textsurface.get_rect()
        self.screen.blit(self.mode_textsurface,(50,80))
        self.running_textsurface = self.running_font.render('State = %s' %self.running_mode, False, (255, 255, 255))
        self.running_rect = self.running_textsurface.get_rect()
        self.screen.blit(self.running_textsurface,(50,150))
        self.limit_textsurface = self.limit_font.render('%d trusses remaining' %(2+self.structure.truss_limit-len(self.structure.trusses)), True, (255, 255, 255))
        self.limit_rect = self.limit_textsurface.get_rect()
        self.limit_topleft = (1200-self.limit_rect[2],80)
        self.screen.blit(self.limit_textsurface,self.limit_topleft)
        #----------------------------
        if self.balls != None:
            self.ball_rolling()
            for ball in self.balls:
                ball_pos = (ball.pos.x-40,ball.pos.y-35)
                self.screen.blit(self.car,ball_pos)            
        for i in structure.nodes:
            if i in self.dltnode:
                i.draw_node(True)
            else:
                i.draw_node(False)
        for i in structure.trusses:
            if i in structure.roadtrusses :
                if not i.collapse:
                    if i in self.dlttruss:
                        i.draw_marked_Truss(True)
                    else:
                        i.draw_marked_Truss(False)
            else:
                if not i.collapse:
                    if i in self.dlttruss:
                        i.draw_Truss(True)        
                    else:
                        i.draw_Truss(False)
        if self.tmpc[0]:
            pygame.draw.circle(screen,(230,230,230),self.tmpc[1],self.tmpc[2],1)
            for i in range(12):
                pygame.draw.circle(screen,(230,230,230),(int(self.tmpc[1][0]+self.tmpc[2]*cos(pi*i/6)),int(self.tmpc[1][1]+self.tmpc[2]*sin(pi*i/6))),5)
        if structure.collapse:
            self.screen.blit(self.fail_textsurface,(1280/2-self.fail_rect[2]/2,960/6))
            
    def game_start_interface(self):
        path1 = os.path.join(self.dir,'start_button.png')
        path2 = os.path.join(self.dir,'exit_button.png')
        #載入start_button
        self.origin_start_button = pygame.image.load(path1).convert_alpha()
        self.start_button_size = (200,100)
        self.start_button = pygame.transform.scale(self.origin_start_button,self.start_button_size)
        self.start_button_topleft = (1280*(0.5)-self.start_button_size[0]/2,960*(0.5)-self.start_button_size[1]/2)
        #載入exit_button
        self.origin_exit_button = pygame.image.load(path2).convert_alpha()
        self.exit_button_size = (200,100)
        self.exit_button = pygame.transform.scale(self.origin_exit_button,self.exit_button_size)
        self.exit_button_topleft = (self.start_button_topleft[0] , self.start_button_topleft[1]+100)
        #標題
        self.title_font = pygame.font.SysFont('Comic Sans MS', 108)
        self.title_textsurface = self.title_font.render('Poly Bridge ', False, (0, 255, 255))
        self.title_rect = self.title_textsurface.get_rect()
        #背景
        path3 = os.path.join(self.dir,'background.png')
        self.origin_background = pygame.image.load(path3).convert_alpha()
        self.background_size = (1280,960)
        self.background = pygame.transform.scale(self.origin_background,self.background_size)
        self.screen.blit(self.background,(0,0))
        #畫上去
        self.screen.blit(self.title_textsurface,(1280/2-self.title_rect[2]/2,960/8))
        self.screen.blit(self.start_button,self.start_button_topleft)
        self.screen.blit(self.exit_button,self.exit_button_topleft)
    def click_start_button(self,downcod):
        if  self.start_button_topleft[0]< downcod[0] < self.start_button_topleft[0]+self.start_button_size[0]:
            if self.start_button_topleft[1] < downcod[1] < self.start_button_topleft[1] + self.start_button_size[1]:
                return True
        return False
    def click_exit_button(self,downcod):
        if self.exit_button_topleft[0] < downcod[0] < self.exit_button_topleft[0]+self.exit_button_size[0]:
            if self.exit_button_topleft[1] < downcod[1] < self.exit_button_topleft[1] + self.exit_button_size[1]:
                return True
        return False
    def esc_interface(self):
        path4 = os.path.join(self.dir,'esc_bg1.png')
        self.origin_esc_bg = pygame.image.load(path4).convert_alpha()
        self.esc_bg = pygame.transform.scale(self.origin_esc_bg,(1280,960))
        self.screen.blit(self.esc_bg,(0,0))
        #resume
        path5 = os.path.join(self.dir,'resume_button.png')
        self.origin_esc_resume_button = pygame.image.load(path5).convert_alpha()
        self.esc_resume_button_size = (200,100)
        self.esc_resume_button = pygame.transform.scale(self.origin_esc_resume_button,self.esc_resume_button_size)
        self.esc_resume_button_topleft = (1280/2-100,960/4)
        self.screen.blit(self.esc_resume_button,self.esc_resume_button_topleft)
        #restart
        path6 = os.path.join(self.dir,'restart_button.png')
        self.origin_esc_restart_button = pygame.image.load(path6).convert_alpha()
        self.esc_restart_button_size = (200,100)
        self.esc_restart_button = pygame.transform.scale(self.origin_esc_restart_button,self.esc_restart_button_size)
        self.esc_restart_button_topleft = (1280/2-100,960/4+100)
        self.screen.blit(self.esc_restart_button,self.esc_restart_button_topleft)
        #exit
        path7 = os.path.join(self.dir,'esc_exit_button.png')
        self.origin_esc_exit_button = pygame.image.load(path7).convert_alpha()
        self.esc_exit_button_size = (200,100)
        self.esc_exit_button = pygame.transform.scale(self.origin_esc_exit_button,self.esc_exit_button_size)
        self.esc_exit_button_topleft = (1280/2-100,960/4+200)
        self.screen.blit(self.esc_exit_button,self.esc_exit_button_topleft)
        #判別是否在esc畫面中
        self.esc_or_not = True
    def click_esc_resume_button(self,downcod):
        if self.esc_resume_button_topleft[0] < downcod[0] < self.esc_resume_button_topleft[0]+self.esc_resume_button_size[0]:
            if self.esc_resume_button_topleft[1] < downcod[1] < self.esc_resume_button_topleft[1] + self.esc_resume_button_size[1]:
                return True
        return False
    def click_esc_restart_button(self,downcod):
        if self.esc_restart_button_topleft[0] < downcod[0] < self.esc_restart_button_topleft[0]+self.esc_restart_button_size[0]:
            if self.esc_restart_button_topleft[1] < downcod[1] < self.esc_restart_button_topleft[1] + self.esc_restart_button_size[1]:
                return True
        return False
    def click_esc_exit_button(self,downcod):
        if self.esc_exit_button_topleft[0] < downcod[0] < self.esc_exit_button_topleft[0]+self.esc_exit_button_size[0]:
            if self.esc_exit_button_topleft[1] < downcod[1] < self.esc_exit_button_topleft[1] + self.esc_exit_button_size[1]:
                return True
        return False
    def game_restart(self):
        new_structure = Structure(self.screen)
        self.__init__(new_structure,self.screen)
    def show_win(self):
        self.win_font = pygame.font.SysFont('Comic Sans MS', 108)
        self.win_textsurface = self.win_font.render('You just won! ', True, (255, 0, 0))
        self.win_rect = self.win_textsurface.get_rect()
        self.note_font = pygame.font.SysFont('Comic Sans MS',50)
        self.note_textsurface = self.note_font.render('PRESS A BUTTON BACK TO MENU!',True,(0,0,0))
        self.note_rect = self.note_textsurface.get_rect()
        self.screen.blit(self.win_textsurface,(1280/2-self.win_rect[2]/2,960/8))
        self.screen.blit(self.note_textsurface,(1280/2-self.note_rect[2]/2,600))
    def findnode(self,mpos):
        structure = self.structure
        self.reltruss = []
        nid = -1
        screen,nodes,click,trusses = structure.screen, structure.nodes, self.click, structure.trusses
        for i in range(len(nodes)):
            check = nodes[i]
            if check.clicked(mpos):
                nid=i
                break
        for tru in trusses:
            if tru.nodeA == nodes[nid] or tru.nodeB == nodes[nid]:
                self.reltruss.append(tru)
        return nid
    def mvnode(self,mpos):
        structure = self.structure
        screen,nodes,click,trusses = structure.screen, structure.nodes, self.click, structure.trusses
        npos = vector(mpos[0],mpos[1],0)
        for tru in self.reltruss:
            if mag(npos-tru.nodeA.pos) > self.tmpc[2] or mag(npos-tru.nodeB.pos) > self.tmpc[2]:
                return
        nodes[self.altednode].pos = npos