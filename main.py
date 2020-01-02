import sys, pygame, copy, time
from pygame.locals import *
from anastruct import SystemElements
from vpython import *
from Node import *
from Truss import *
from Bio import *
from Ball import *
from Controller import *

pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()

width, height = 1280, 960
screen = pygame.display.set_mode((width, height))
# Game loop.
screen.fill((255,255,255))
main_structure = Structure(screen)
main_controller = Controller(main_structure,screen)
main_controller.initail_platform()

#main_structure.create()

while True:
    psedkey=pygame.key.get_pressed()
    psedmse=pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT:
            main_structure.print_result()
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONUP :
            upcod = pygame.mouse.get_pos() 
            if not main_controller.dlt:
                main_controller.clicked(MOUSEBUTTONUP,upcod,event.button)
            if main_controller.dlt and event.button == 3:
                main_controller.dltcod[1]=upcod
                print(main_controller.dltcod)
                main_controller.delarea()

        if event.type == MOUSEBUTTONDOWN:
            downcod = pygame.mouse.get_pos()
            if not main_controller.dlt:
                main_controller.clicked(MOUSEBUTTONDOWN,downcod,event.button)
            if main_controller.dlt and event.button == 3:
                main_controller.dltcod[0]=downcod
        if event.type == KEYUP:
            if event.key == K_d:
                main_controller.dlt=False
        if event.type == KEYDOWN:
            if event.key == K_d:
                main_controller.dlt=True
            if event.key == K_SPACE:
                main_controller.add_ball()
            if event.key == K_1:
                main_controller.mode=0
                print('mode1')
            if event.key == K_2:
                main_controller.mode=1
                print('mode2')
            if event.key == K_LSHIFT or event.key == K_RSHIFT:
                if not main_controller.first :
                    main_controller.structure_save()
                    main_controller.first = True
                    print("saved")
                if not main_controller.running:
                    main_controller.running = True
                    print("running")
                else:
                    main_controller.running = False
                    print('stop')
            if event.key == K_4:
                main_controller.structure_reset()
                
    # Update.
    main_controller.update()

    if main_structure.collapse:
        for test in main_controller.Bios:
            test.ground_collision()
            test.system_check_collision(main_controller.Bios)
            test.time_lapse()
            test.draw_Truss(screen)
            test.draw_node(screen)
    # Draw.
    pygame.display.flip()
    fpsClock.tick(fps)
