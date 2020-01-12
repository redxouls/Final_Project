import sys, pygame, time, copy, os
import numpy as np
from pygame.locals import *
from anastruct import SystemElements
from vpython import *
from Ball import *
from Node import *
from Truss import *
from Bio import *
from Structure import *
from Controller import *


class Map:
    def __init__(self,id):
        self.id = id
        self.controller = Controller()

    def initial_platform(self):
        structure = self.structure
        left_nodeA = structure.add_node(0,700)
        left_nodeB = structure.add_node(200,700)
        structure.add_truss(left_nodeA,left_nodeB,0)
        right_nodeA = structure.add_node(1080,700)
        right_nodeB = structure.add_node(1280,700)
        structure.add_truss(right_nodeA,right_nodeB,0)
        