import sys, pygame, structure
import numpy as np
from pygame.locals import *
import anaconv
from anastruct import SystemElements
#import matplotlib.pyplot as plt

screen = None

# Game loop.
main_structure = structure.Structure(screen)
main_structure.create()
main_structure.trusses=anaconv.visualize(main_structure, main_structure.nodes,main_structure.trusses)
