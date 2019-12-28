import sys, pygame, structure, copy, time
from pygame.locals import *
from anastruct import SystemElements
from vpython import *
from Node import *
from Truss import *
from Bio import *
from ball import *

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
main_structure.initail_platform()
#main_structure.create()

while True:
    for event in pygame.event.get():
        #print(event.type)
        if event.type == QUIT:
            main_structure.print_result()
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
                print('mode1')
            if event.key == K_2:
                main_structure.mode=1
                print('mode2')
            if event.key == K_3:
                for test in main_structure.Bios:
                    test.time_lapse()
                    test.ground_collision()
                    test.system_check_collision(main_structure.Bios)
            if event.key == K_LSHIFT or event.key == K_RSHIFT:
                if not main_structure.first :
                    main_structure.structure_save()
                    main_structure.first = True
                    print("saved")
                if not main_structure.running:
                    main_structure.running = True
                    print("running")
                else:
                    main_structure.running = False
                    print('stop')
            if event.key == K_4:
                main_structure.structure_reset()
                

                
    # Update.
    main_structure.update()

    if main_structure.collapse:
        for test in main_structure.Bios:
            test.ground_collision()
            test.system_check_collision(main_structure.Bios)
            test.time_lapse()
            test.draw_Truss(screen)
            test.draw_node(screen)
    # Draw.
    pygame.display.flip()
    fpsClock.tick(fps)