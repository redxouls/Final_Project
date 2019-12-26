import sys, pygame, structure, copy, time
from pygame.locals import *
from anastruct import SystemElements
from vpython import *
import NodeTruss

size, m_o, m_c, k_bond = 30, 20, 20, 18600.0    # These numbers are all made up
d = 2.5*size
dt = 0.1

pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()

width, height = 1280, 960
screen = pygame.display.set_mode((width, height))
# Game loop.
screen.fill((255,255,255))
main_structure = structure.Structure(screen)

#main_structure.create()
COs = []
for i in range(3):
    COs.append(NodeTruss.Bio(pos=vector(150+i*10, 350+i*100, 0), axis = vector(d, 0, 0),screen = screen,d=d))

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
            if event.key == K_SPACE:
                main_structure.add_ball()
            if event.key == K_1:
                main_structure.mode=0
            if event.key == K_2:
                main_structure.mode=1
    # Update.
    main_structure.update()
    '''
    for test in COs:
        test.draw_Truss()
        test.draw_node()
        test.time_lapse(dt)
        test.ground_collision()
        test.system_check_collision(COs)
    '''               
    # Draw.
    pygame.display.flip()
    fpsClock.tick(fps)