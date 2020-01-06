import sys, pygame, copy, time
from pygame.locals import *
from anastruct import SystemElements
from vpython import *
from Node import *
from Truss import *
from Bio import *
from Ball import *
from Controller import *
from Structure import *

pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()

width, height = 1280, 960
screen = pygame.display.set_mode((width, height))
# Game loop.
screen.fill((255,255,255))
main_structure = Structure(screen)
main_controller = Controller(main_structure,screen)


while True:
    #初始介面
    if not main_controller.game_running:
        main_controller.game_start_interface()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                downcod = pygame.mouse.get_pos()
                if main_controller.click_start_button(downcod):
                    main_controller.game_running = True

                if main_controller.click_exit_button(downcod):
                    pygame.quit()
                    sys.exit()
    #in the game
    if  main_controller.game_running and not main_controller.esc_or_not:
        if main_controller.first_time:
            main_controller.initail_platform()
        
        psedkey=pygame.key.get_pressed()
        psedmse=pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                main_controller.structure.print_result()
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP :
                if not main_controller.first_click :
                    main_controller.tmpc[0]=False
                    upcod = pygame.mouse.get_pos() 
                    if not main_controller.dlt:
                        main_controller.clicked(MOUSEBUTTONUP,upcod,event.button)
                    if main_controller.dlt and event.button == 3:
                        main_controller.dltcod[1]=upcod
                        print(main_controller.dltcod)
                        main_controller.delarea()
                main_controller.first_click = False

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
                    main_controller.dltnode=[]
                    main_controller.dlttruss=[]
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
                    if not main_controller.running:
                        main_controller.structure_save()
                        main_controller.first = True
                        print("saved")
                        main_controller.running = True
                        print("running")
                    else:
                        main_controller.running = False
                        print('stop')
                if event.key == K_4:
                    main_controller.structure_reset()
                if event.key == K_ESCAPE:
                    main_controller.esc_interface()
                if event.key == K_BACKSPACE:
                    main_controller.clear()
                if event.key == K_e:
                    main_controller.recov()

        main_controller.first_time = False
        
        if not main_controller.esc_or_not:
            main_controller.update()
        
    ##esc(in the game)
    if main_controller.game_running and main_controller.esc_or_not:  
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                downcod = pygame.mouse.get_pos()
                if main_controller.click_esc_exit_button(downcod):
                    pygame.quit()
                    sys.exit()
                if main_controller.click_esc_restart_button(downcod):
                    main_controller.first_click = True
                    main_controller.esc_or_not = False
                    #####need to be fixed
                    main_controller.game_restart()
                    main_controller.initail_platform()
                    ######
                if main_controller.click_esc_resume_button(downcod):
                    main_controller.first_click = True
                    main_controller.esc_or_not = False
        

    if main_controller.structure.collapse and main_controller.game_running and not main_controller.esc_or_not:
        for test in main_controller.Bios:
            test.ground_collision()
            test.system_check_collision(main_controller.Bios)
            test.time_lapse()
            test.draw_Truss(screen)
            test.draw_node(screen)
    # Draw.
    #if main_controller.game_running:
    pygame.display.flip()
    fpsClock.tick(fps)
