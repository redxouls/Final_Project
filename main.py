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
    if not main_controller.game_running and not  main_controller.choose_map:
        main_controller.game_start_interface()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                downcod = pygame.mouse.get_pos()
                if main_controller.click_start_button(downcod):
                    main_controller.game_running = False
                    main_controller.choose_map = True

                if main_controller.click_exit_button(downcod):
                    pygame.quit()
                    sys.exit()
    if not main_controller.game_running and main_controller.choose_map:
        main_controller.choose_map_interface()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                downcod = pygame.mouse.get_pos()
                if main_controller.click_map1_button(downcod):
                    main_controller.map = 1
                    main_controller.game_running = True
                    main_controller.first_click = True
                if main_controller.click_map2_button(downcod):
                    main_controller.map = 2
                    main_controller.game_running = True
                    main_controller.first_click = True
                if main_controller.click_map3_button(downcod):
                    main_controller.map = 3
                    main_controller.game_running = True
                    main_controller.first_click = True  
    #in the game
    if  main_controller.game_running and not main_controller.esc_or_not and not main_controller.win and not main_controller.button_help:
        if main_controller.first_time:
            main_controller.initial_platform(main_controller.map)
            main_controller.first_time = False
        
        psedkey=pygame.key.get_pressed()
        psedmse=pygame.mouse.get_pressed()
        if main_controller.alt[0] and psedmse[2]:
            if main_controller.altednode != -1:
                main_controller.mvnode(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == QUIT:
                main_controller.structure.print_result()
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP :
                main_controller.tmpc[0]=False
                if not main_controller.first_click :
                    upcod = pygame.mouse.get_pos() 
                    if not (main_controller.dlt or main_controller.alt[0]):
                        main_controller.clicked(MOUSEBUTTONUP,upcod,event.button)
                    if main_controller.dlt and event.button == 3:
                        main_controller.dltcod[1]=upcod
                        main_controller.delarea()
                main_controller.first_click = False

            if event.type == MOUSEBUTTONDOWN:
                downcod = pygame.mouse.get_pos()
                if not (main_controller.dlt or main_controller.alt[0]):
                    main_controller.clicked(MOUSEBUTTONDOWN,downcod,event.button)
                if main_controller.dlt and event.button == 3:
                    main_controller.dltcod[0]=downcod
                if main_controller.alt[0]:
                    main_controller.altednode = main_controller.findnode(downcod)
            if event.type == KEYUP:
                if event.key == K_d:
                    main_controller.dlt=False
                if event.key == K_a:
                    main_controller.alt[0] =False
            if event.type == KEYDOWN:
                if event.key == K_d:
                    main_controller.dltnode=[]
                    main_controller.dlttruss=[]
                    main_controller.dlt=True
                if event.key == K_SPACE:
                    main_controller.add_ball()
                if event.key == K_1:
                    main_controller.mode=0
                if event.key == K_2:
                    main_controller.mode=1
                if event.key == K_LSHIFT or event.key == K_RSHIFT:
                    if not main_controller.running:
                        main_controller.structure.set_orilen()
                        main_controller.structure_save()
                        main_controller.first = True
                        main_controller.running = True
                    else:
                        main_controller.running = False
                if event.key == K_4:
                    main_controller.structure_reset()
                if event.key == K_ESCAPE:
                    main_controller.esc_interface()
                if event.key == K_BACKSPACE:
                    main_controller.clear()
                if event.key == K_e:
                    main_controller.recov()
                if event.key == K_a:
                    main_controller.alt[0] = True
                if event.key == K_s:
                    main_controller.structure.output()
                if event.key == K_l:
                    main_controller.structure.load()
        main_controller.first_time = False
        
        if not main_controller.esc_or_not:
            main_controller.update()
    if main_controller.game_running and not main_controller.esc_or_not and main_controller.win and not main_controller.button_help:
        main_controller.show_win()
        
        main_controller.running = False
       
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                main_controller.win = False
                main_controller.game_running = False
                main_controller.game_restart()
    ##esc(in the game)
    if main_controller.game_running and main_controller.esc_or_not and not main_controller.button_help:  
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
                    ######
                if main_controller.click_esc_resume_button(downcod):
                    main_controller.first_click = True
                    main_controller.esc_or_not = False

                if main_controller.click_help(downcod):
                    main_controller.first_click = True
                    main_controller.button_help = True
                    main_controller.esc_or_not = False
        
    if main_controller.game_running and not main_controller.esc_or_not and main_controller.button_help:
        main_controller.help_interface()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                main_controller.first_click = True
                main_controller.button_help = False

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
