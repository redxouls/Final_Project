import sys, pygame, structure, copy, time
from pygame.locals import *
from anastruct import SystemElements

pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()

width, height = 1280, 960
screen = pygame.display.set_mode((width, height))
# Game loop.
screen.fill((255,255,255))
main_structure = structure.Structure(screen)

#main_structure.create()

while True:
  for event in pygame.event.get():
    if event.type == QUIT:
        main_structure.print_result()
        print(main_structure.two_end())
        pygame.quit()
        sys.exit()
    if event.type == MOUSEBUTTONUP :
        upcod = pygame.mouse.get_pos() 
        main_structure.clicked(MOUSEBUTTONUP,upcod,event.button)

    if event.type == MOUSEBUTTONDOWN:
        downcod = pygame.mouse.get_pos()
        main_structure.clicked(MOUSEBUTTONDOWN,downcod,event.button)

    if event.type == KEYDOWN:
      main_structure.add_ball()
  # Update.
  main_structure.update()
  # Draw.
  pygame.display.flip()
  fpsClock.tick(fps)