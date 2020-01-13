import sys, pygame, time, copy, os, json
import numpy as np
from pygame.locals import *
from anastruct import SystemElements
from vpython import *
from Ball import *
from Node import *
from Truss import *
from Bio import *
from Structure import *
import Car

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
        self.lose = False
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
        self.car_position = vector(0,0,0)
        self.mkts = []
        self.choose_map = False
        self.button_help = False
    def add_ball(self):
        self.car_position = vector(30,self.structure.nodes[0].pos.y-90,0)
        new_balls = [Ball(self.screen,len(self.balls),self.car_position),Ball(self.screen,len(self.balls),self.car_position)]
        self.structure.loadid.append([])
        self.balls.append(new_balls)
        self.mkts.append(Car.BouncyBalls(self,self.car_position))

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
            return
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
        structure = self.structure
        for mkt in self.mkts:
            mkt.run()
            for ballpair in self.balls:
                #print(ballpair[0].ground_distance(self.structure),ballpair[1].ground_distance(self.structure))
                if ballpair[0].ground_distance(self.structure)!=None:
                    if abs(ballpair[0].ground_distance(self.structure)-25)<1:
                        structure.loadid[ballpair[0].label] = [structure.nodes.index(structure.trusses[ballpair[0].nearest(structure)].nodeA),structure.nodes.index(structure.trusses[ballpair[0].nearest(structure)].nodeB)]
                    else:
                        structure.loadid[ballpair[0].label] = []
                if ballpair[1].ground_distance(self.structure)!=None:
                    if abs(ballpair[1].ground_distance(self.structure)-25)<1:
                        structure.loadid[ballpair[1].label] = [structure.nodes.index(structure.trusses[ballpair[1].nearest(structure)].nodeA),structure.nodes.index(structure.trusses[ballpair[1].nearest(structure)].nodeB)]
                    else:
                        structure.loadid[ballpair[0].label] = []
                if ballpair[0].pos.x>1200 and ballpair[0].pos.y<960 and ballpair[0].pos.y>0:
                    self.win = True
                if ballpair[0].pos.x<1200 and ballpair[0].pos.y>=960:
                    self.lose = True

    def structure_save(self):
        if self.structure.collapse:
            return
        structure = self.structure
        structure.tempnodespos =[0]*len(structure.nodes) 
        for i in range(len(structure.nodes)):
            structure.tempnodespos[i] = structure.nodes[i].pos

    def structure_reset(self):
        structure = self.structure
        if structure.tempnodespos == [] or len(structure.tempnodespos)!=len(structure.nodes):
            return
        structure.loadid = []
        structure.collapse = False
        self.lose = False
        self.running = False
        self.balls  = []
        self.Bios = []
        for i in range(len(structure.tempnodespos)):
            structure.nodes[i].pos = structure.tempnodespos[i]
        for i in range(len(structure.trusses)):
            structure.trusses[i].collapse = False
        structure.set_orilen()
    
    def check_collapse(self):
        structure = self.structure
        collpase = False
        for truss in structure.trusses:
            if truss.length()>truss.oril+3:
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

    def initial_platform(self,mapid):
        structure = self.structure
        if mapid == 1:
            self.car_position = vector(60,650,0)
            structure.truss_limit = 25
            left_nodeA = structure.add_node(0,700)
            left_nodeB = structure.add_node(200,700)
            structure.add_truss(left_nodeA,left_nodeB,0)
            right_nodeA = structure.add_node(1080,200)
            right_nodeB = structure.add_node(1280,200)
            structure.add_truss(right_nodeA,right_nodeB,0)
            return
        if mapid == 2:
            self.car_position = vector(60,150,0)
            structure.truss_limit = 25
            left_nodeA = structure.add_node(0,200)
            left_nodeB = structure.add_node(200,200)
            structure.add_truss(left_nodeA,left_nodeB,0)
            right_nodeA = structure.add_node(1080,700)
            right_nodeB = structure.add_node(1280,700)
            structure.add_truss(right_nodeA,right_nodeB,0)
            return
        if mapid ==3:
            left_nodeA = structure.add_node(0,700)
            left_nodeB = structure.add_node(200,700)
            structure.add_truss(left_nodeA,left_nodeB,0)
            right_nodeA = structure.add_node(1080,700)
            right_nodeB = structure.add_node(1280,700)
            structure.add_truss(right_nodeA,right_nodeB,0)
            ob_node_la1 = structure.add_obnode(500,960)
            ob_node_lb1 = structure.add_obnode(500,560)
            structure.add_obstruss(ob_node_la1,ob_node_lb1)
            ob_node_la2 = structure.add_obnode(500,560)
            ob_node_lb2 = structure.add_obnode(600,460)
            structure.add_obstruss(ob_node_la2,ob_node_lb2)
            ob_node_ra1 = structure.add_obnode(600,460)
            ob_node_rb1 = structure.add_obnode(700,560)
            structure.add_obstruss(ob_node_ra1,ob_node_rb1)
            ob_node_ra2 = structure.add_obnode(700,560)
            ob_node_rb2 = structure.add_obnode(700,960)
            structure.add_obstruss(ob_node_ra2,ob_node_rb2)
            return
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
            print('unstable')
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
        if self.balls != None and self.running:
            self.ball_rolling()
        for i in structure.nodes:
            if i in self.dltnode:
                i.draw_node(True)
            else:
                i.draw_node(False)
        for i in structure.obnode:
            i.draw_obnode()
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
        for i in structure.obtruss:
            i.draw_obtruss()
        if self.tmpc[0]:
            pygame.draw.circle(screen,(230,230,230),self.tmpc[1],self.tmpc[2],1)
            for i in range(12):
                pygame.draw.circle(screen,(230,230,230),(int(self.tmpc[1][0]+self.tmpc[2]*cos(pi*i/6)),int(self.tmpc[1][1]+self.tmpc[2]*sin(pi*i/6))),5)
        if structure.collapse or self.lose:
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
        if  self.start_button_topleft[0]+15< downcod[0] < self.start_button_topleft[0]+self.start_button_size[0]-20:
            if self.start_button_topleft[1]+15 < downcod[1] < self.start_button_topleft[1] + self.start_button_size[1]-20:
                return True
        return False
    def click_exit_button(self,downcod):
        if self.exit_button_topleft[0]+15 < downcod[0] < self.exit_button_topleft[0]+self.exit_button_size[0]-20:
            if self.exit_button_topleft[1]+15 < downcod[1] < self.exit_button_topleft[1] + self.exit_button_size[1]-20:
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
        self.esc_exit_button_topleft = (1280/2-100,960/4+300)
        self.screen.blit(self.esc_exit_button,self.esc_exit_button_topleft)
        #判別是否在esc畫面中
        self.esc_or_not = True
        ########3
        path15 = os.path.join(self.dir,'help.png')
        self.origin_help_button = pygame.image.load(path15).convert_alpha()
        self.help_button_size = (200,100)
        self.help_button = pygame.transform.scale(self.origin_help_button,self.help_button_size)
        self.help_button_topleft = (1280/2-100,960/4+200)
        self.screen.blit(self.help_button,self.help_button_topleft) 
    def click_esc_resume_button(self,downcod):
        if self.esc_resume_button_topleft[0]+15 < downcod[0] < self.esc_resume_button_topleft[0]+self.esc_resume_button_size[0]-20:
            if self.esc_resume_button_topleft[1]+15 < downcod[1] < self.esc_resume_button_topleft[1] + self.esc_resume_button_size[1]-20:
                return True
        return False
    def click_esc_restart_button(self,downcod):
        if self.esc_restart_button_topleft[0]+15 < downcod[0] < self.esc_restart_button_topleft[0]+self.esc_restart_button_size[0]-20:
            if self.esc_restart_button_topleft[1]+15 < downcod[1] < self.esc_restart_button_topleft[1] + self.esc_restart_button_size[1]-20:
                return True
        return False
    def click_esc_exit_button(self,downcod):
        if self.esc_exit_button_topleft[0]+15 < downcod[0] < self.esc_exit_button_topleft[0]+self.esc_exit_button_size[0]-20:
            if self.esc_exit_button_topleft[1]+15 < downcod[1] < self.esc_exit_button_topleft[1] + self.esc_exit_button_size[1]-20:
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
        if nid <=3:
            return -1
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
    
    def choose_map_interface(self):
        path3 = os.path.join(self.dir,'background.png')
        self.origin_background = pygame.image.load(path3).convert_alpha()
        self.background_size = (1280,960)
        self.background = pygame.transform.scale(self.origin_background,self.background_size)
        self.screen.blit(self.background,(0,0))
        
        self.map_font = pygame.font.SysFont('Comic Sans MS', 70)
        self.map_textsurface = self.map_font.render('Choose Your Map!! ', True, (255, 0, 0))
        self.map_rect = self.map_textsurface.get_rect()
        self.screen.blit(self.map_textsurface,(1280/2-self.map_rect[2]/2,960/8))
        
        path11 = os.path.join(self.dir,'map1.png')
        self.origin_map1_button = pygame.image.load(path11).convert_alpha()
        self.map1_button_size = (200,100)
        self.map1_button = pygame.transform.scale(self.origin_map1_button,self.map1_button_size)
        
        self.map1_button_topleft = (1280/2-100,960/4+100)##########
        self.screen.blit(self.map1_button,self.map1_button_topleft)

        path12 = os.path.join(self.dir,'map2.png')
        self.origin_map2_button = pygame.image.load(path12).convert_alpha()
        self.map2_button_size = (200,100)
        self.map2_button = pygame.transform.scale(self.origin_map2_button,self.map2_button_size)
        self.map2_button_topleft = (1280/2-100,960/4+200)############
        self.screen.blit(self.map2_button,self.map2_button_topleft)

        path13 = os.path.join(self.dir,'map3.png')
        self.origin_map3_button = pygame.image.load(path13).convert_alpha()
        self.map3_button_size = (200,100)
        self.map3_button = pygame.transform.scale(self.origin_map3_button,self.map3_button_size)
        self.map3_button_topleft = (1280/2-100,960/4+300)##############
        self.screen.blit(self.map3_button,self.map3_button_topleft)


    def click_map1_button(self,downcod):
        if self.map1_button_topleft[0] +15< downcod[0] < self.map1_button_topleft[0]+self.map1_button_size[0] -15:
            if self.map1_button_topleft[1]+20 < downcod[1] < self.map1_button_topleft[1] + self.map1_button_size[1]-20:
                return True
    def click_map2_button(self,downcod):
        if self.map2_button_topleft[0]+15 < downcod[0] < self.map2_button_topleft[0]+self.map2_button_size[0]-15:
            if self.map2_button_topleft[1]+20 < downcod[1] < self.map2_button_topleft[1] + self.map2_button_size[1]-20:
                return True
    def click_map3_button(self,downcod):
        if self.map3_button_topleft[0]+15 < downcod[0] < self.map3_button_topleft[0]+self.map3_button_size[0]-15:
            if self.map3_button_topleft[1]+20 < downcod[1] < self.map3_button_topleft[1] + self.map3_button_size[1]-20:
                return True
    def click_help(self,downcod):
        if self.help_button_topleft[0] < downcod[0] < self.help_button_topleft[0]+self.help_button_size[0]:
            if self.help_button_topleft[1] < downcod[1] < self.help_button_topleft[1] + self.help_button_size[1]:
                return True

    def help_interface(self):
        path4 = os.path.join(self.dir,'esc_bg1.png')
        self.origin_esc_bg = pygame.image.load(path4).convert_alpha()
        self.esc_bg = pygame.transform.scale(self.origin_esc_bg,(1280,960))
        self.screen.blit(self.esc_bg,(0,0))

        self.con_font = pygame.font.SysFont('Comic Sans MS',50)
        self.con_textsurface = self.con_font.render('CLICK TO BACK TO THE GAME',True,(0,0,0))
        self.con_rect = self.con_textsurface.get_rect()
        self.screen.blit(self.con_textsurface,(1280/2-self.con_rect[2]/2,700))

        path20 = os.path.join(self.dir,'1.png')
        self.origin_image_1 = pygame.image.load(path20).convert_alpha()
        self.image_1 = pygame.transform.scale(self.origin_image_1,(90,60))
        self.screen.blit(self.image_1,(100,50))

        path21 = os.path.join(self.dir,'2.png')
        self.origin_image_2 = pygame.image.load(path21).convert_alpha()
        self.image_2 = pygame.transform.scale(self.origin_image_2,(90,60))
        self.screen.blit(self.image_2,(100,130))

        path22 = os.path.join(self.dir,'4.png')
        self.origin_image_3 = pygame.image.load(path22).convert_alpha()
        self.image_3 = pygame.transform.scale(self.origin_image_3,(90,60))
        self.screen.blit(self.image_3,(100,210))

        path23 = os.path.join(self.dir,'D.png')
        self.origin_image_D = pygame.image.load(path23).convert_alpha()
        self.image_D = pygame.transform.scale(self.origin_image_D,(90,60))
        self.screen.blit(self.image_D,(100,290))

        path24 = os.path.join(self.dir,'backspace1.png')
        self.origin_image_backspace = pygame.image.load(path24).convert_alpha()
        self.image_backspace = pygame.transform.scale(self.origin_image_backspace,(120,40))
        self.screen.blit(self.image_backspace,(100,380))

        path26 = os.path.join(self.dir,'s.png')
        self.origin_image_s = pygame.image.load(path26).convert_alpha()
        self.image_s = pygame.transform.scale(self.origin_image_s,(90,60))
        self.screen.blit(self.image_s,(100,460))

        path29= os.path.join(self.dir,'l.png')
        self.origin_image_l = pygame.image.load(path29).convert_alpha()
        self.image_l = pygame.transform.scale(self.origin_image_l,(90,60))
        self.screen.blit(self.image_l,(100,540))

        path30= os.path.join(self.dir,'shift.png')
        self.origin_image_shift = pygame.image.load(path30).convert_alpha()
        self.image_shift = pygame.transform.scale(self.origin_image_shift,(120,40))
        self.screen.blit(self.image_shift,(100,620))

        self._1_font = pygame.font.SysFont('Comic Sans MS', 30)
        self._1_textsurface = self._1_font.render('Floor Mode ', False, (255, 255, 255))
        self.screen.blit(self._1_textsurface,(300,50))

        self._2_font = pygame.font.SysFont('Comic Sans MS', 30)
        self._2_textsurface = self._2_font.render('Wood Mode ', False, (255, 255, 255))
        self.screen.blit(self._2_textsurface,(300,130))

        self._4_font = pygame.font.SysFont('Comic Sans MS', 30)
        self._4_textsurface = self._4_font.render('Reset', False, (255, 255, 255))
        self.screen.blit(self._4_textsurface,(300,210))

        self._d_font = pygame.font.SysFont('Comic Sans MS', 30)
        self._d_textsurface = self._d_font.render('Hold D and select the area you want to delete ', False, (255, 255, 255))
        self.screen.blit(self._d_textsurface,(300,290))

        self.backspace_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.back_textsurface = self.backspace_font.render('After selecting the area, press backspace to remove the structure',False,(255,255,255))
        self.screen.blit(self.back_textsurface,(300,380))

        self.s_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.s_textsurface = self.s_font.render('Save structure',False,(255,255,255))
        self.screen.blit(self.s_textsurface,(300,460))

        self.l_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.l_textsurface = self.l_font.render('Load previous structure',False,(255,255,255))
        self.screen.blit(self.l_textsurface,(300,540))

        self.shift_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.shift_textsurface = self.shift_font.render('Stop / Running', False, (255, 255, 255))
        self.screen.blit(self.shift_textsurface,(300,620))
    