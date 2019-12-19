import sys, pygame, structure
import numpy as np
from pygame.locals import *
import anaconv
from anastruct import SystemElements
#import matplotlib.pyplot as plt
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()

width, height = 1280, 960
screen = pygame.display.set_mode((width, height))

# Game loop.
screen.fill((255,255,255))
main_structure = structure.Structure(screen)
main_structure.create()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            main_structure.print_result()
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONUP and main_structure.click[0]:
            upcod = pygame.mouse.get_pos() 
            main_structure.clicked(MOUSEBUTTONUP,upcod)
        if event.type == MOUSEBUTTONDOWN:
            downcod = pygame.mouse.get_pos()
            main_structure.clicked(MOUSEBUTTONDOWN,downcod)
        #print(main_structure.trusses[0].nodeA.cod)
        main_structure.update()
        main_structure.trusses=anaconv.visualize(main_structure.nodes,main_structure.trusses)
  # Update.
  
  # Draw.
  
    pygame.display.flip()
    fpsClock.tick(fps)
