import sys
import pygame
from pygame.locals import *

class dot :
    def __init__(self,x=0,y =0,screen=None):
        self.x = x
        self.y = y
        self.cod = [x,y]
        self.r = 10
        self.screen = screen
        self.draw_dot(screen)
    def draw_dot(self,screen):
        pygame.draw.circle(screen, (0, 127, 255), self.cod, self.r, 0)
    def clicked(self,mouse_pos):
        distance = ((self.x-mouse_pos[0])**2+(self.y-mouse_pos[1])**2)**0.5
        if distance <= self.r:
            return True
        else:
            return False
class line(dot):
    def __init__(self,dotA=None,dotB=None,screen=None):
        self.dotA = dotA
        self.dotB = dotB
        self.screen = screen
    def draw_line(self,screen):
        pygame.draw.line(self.screen,(0,0,0), self.dotA.cod, self.dotB.cod, 3)

class structure:
    def __init__(self,screen):
        self.lines = []
        self.dots = []
        self.click = [False,0]
        self.screen = screen
    def add(self,newline=None,newdot=None):
        if newline!= None:
            self.lines.append(newline)
        if newdot!= None:
            self.lines.append(newdot)
    def length(self,choice):
        if choice == 'dots':
            return len(self.dotss)
        if choice == 'lines':
            return len(self.lines)
    def print_result(self):
        dots = self.dots
        lines = self.lines
        for i in range(len(dots)):
            print('dots: ',i,dots[i].cod)
        for i in range(len(lines)):
            print('lines: ',i,lines[i].dotA.cod,'linkto',i,lines[i].dotB.cod)
    def clicked(self,event_type,mouse_pos):
        screen = self.screen
        dots = self.dots
        click = self.click
        lines = self.lines
        downcod , upcod = mouse_pos, mouse_pos
        if event_type == MOUSEBUTTONDOWN:
            for i in range(len(dots)):
                checkdown = dots[i]
                self.click[0] = checkdown.clicked(downcod)
                if self.click[0]:
                    self.click[0],self.click[1] = True , i
                    break
            if not click[0]:
                dots.append(dot(x =downcod[0],y=downcod[1],screen=screen))
        if event_type == MOUSEBUTTONUP:
            upclick = False
            for i in range(len(dots)):
                check = dots[i]
                if check.clicked(upcod):
                    lines.append(line(dots[i],dots[click[1]],screen=screen))
                    lines[-1].draw_line(screen)
                    upclick = True
                    break
            if not upclick:
                dots.append(dot(x=upcod[0],y=upcod[1],screen=screen))
                lines.append(line(dots[-1],dots[click[1]],screen=screen))
                lines[-1].draw_line(screen)
    def update(self):
        pass