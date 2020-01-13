"""This example spawns (bouncing) balls randomly on a L-shape constructed of 
two segment shapes. Not interactive.
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

# Python imports
import random

# Library imports
import pygame
from pygame.key import *
from pygame.locals import *
from pygame.color import *

# pymunk imports
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
#from Controller import *
from Structure import *

from vpython import *


class BouncyBalls(object):
    """
    This class implements a simple scene in which there is a static platform (made up of a couple of lines)
    that don't move. Balls appear occasionally and drop onto the platform. They bounce around.
    """
    def __init__(self,controller,pos):
        self.controller = controller
        self.structure = controller.structure
        self.pos = pos
        # Space
        self._space = pymunk.Space()
        self._space.gravity = (0.0, -900.0)

        # Physics
        # Time step
        self._dt = 1.0 / 60.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 1

        self._draw_options = pymunk.pygame_util.DrawOptions(self.structure.screen)
        
        self.trusses = []
        for i in self.structure.roadtrusses:
            self.trusses.append([(int(i.nodeA.pos.x),960-int(i.nodeA.pos.y)),(int(i.nodeB.pos.x),960-int(i.nodeB.pos.y))])
        # Static barrier walls (lines) that the balls bounce off of
        self._add_static_scenery()

        # Balls that exist in the world
        self._balls = []

        # Execution control and time until the next ball spawns
        self._running = True
        self._ticks_to_next_ball = 10
        self._update_balls()

    def run(self):
        self._add_static_scenery()
        for x in range(self._physics_steps_per_frame):
            self._space.step(self._dt)
        if self.controller.balls == []:
            return
        count = 0
        for i in range(len(self._space.bodies)):
            if self._space.bodies[i].mass!=150:        
                ball1_x = float(self._space.bodies[i].position[0])
                ball1_y = 960-float(self._space.bodies[i].position[1])
                self.controller.balls[0][count].pos = vector(ball1_x,ball1_y,0)
                count+=1
            else:
                continue
        self._draw_objects()


    def _add_static_scenery(self):
        """
        Create the static bodies.
        :return: None
        """
        static_body = self._space.static_body
        self.trusses = []
        for i in self.structure.roadtrusses:
            self.trusses.append([(int(i.nodeA.pos.x),960-int(i.nodeA.pos.y)),(int(i.nodeB.pos.x),960-int(i.nodeB.pos.y))])
        rt=self.trusses
        static_lines=[]
        if len(self._space.shapes)!=0:
            for i in self._space.shapes:
                if hasattr(i,'a'):
                    self._space._remove_shape(i)
        if self.structure.collapse:
            return
        for i in range(len(rt)):
            nl=pymunk.Segment(static_body, rt[i][0], rt[i][1], 0.0)
            static_lines.append(nl)
        for line in static_lines:
            line.elasticity = 0.95
            line.friction = 0.9
        self._space.add(static_lines)

    def _update_balls(self):
        """
        Create/remove balls as necessary. Call once per frame only.
        :return: None
        """
        self._create_ball(self.pos)
       

    def _create_ball(self,setpos=None):
        """
        Create a ball.
        :return:
        """
        if setpos == None:
            return
        else :
            pos = Vec2d(setpos.x,960-setpos.y)
        wheel_color = 52,219,119
        shovel_color = 219,119,52
        mass = 100
        radius = 25
        moment = pymunk.moment_for_circle(mass, 20, radius)
        wheel1_b = pymunk.Body(mass, moment)
        wheel1_s = pymunk.Circle(wheel1_b, radius)
        wheel1_s.friction = 1.5
        wheel1_s.color = wheel_color
        self._space.add(wheel1_b, wheel1_s)

        mass = 100
        radius = 25
        moment = pymunk.moment_for_circle(mass, 20, radius)
        wheel2_b = pymunk.Body(mass, moment)
        wheel2_s = pymunk.Circle(wheel2_b, radius)
        wheel2_s.friction = 1.5
        wheel2_s.color = wheel_color
        self._space.add(wheel2_b, wheel2_s)

        mass = 150
        size = (50,30)
        moment = pymunk.moment_for_box(mass, size)
        chassi_b = pymunk.Body(mass, moment)
        chassi_s = pymunk.Poly.create_box(chassi_b, size)
        self._space.add(chassi_b, chassi_s)


        wheel1_b.position = pos - (55,0)
        wheel2_b.position = pos + (55,0)
        chassi_b.position = pos - (0,-25)

        self._space.add(
            pymunk.PinJoint(wheel1_b, chassi_b, (0,0), (-25,-15)),
            pymunk.PinJoint(wheel1_b, chassi_b, (0,0), (-25, 15)),
            pymunk.PinJoint(wheel2_b, chassi_b, (0,0), (25,-15)),
            pymunk.PinJoint(wheel2_b, chassi_b, (0,0), (25, 15))
            )
        
        speed = -10
        self._space.add(
            pymunk.SimpleMotor(wheel1_b, chassi_b, speed),
            pymunk.SimpleMotor(wheel2_b, chassi_b, speed)
        )

    def _draw_objects(self):
        """
        Draw the objects.
        :return: None
        """
        self._space.debug_draw(self._draw_options)

def main(controller,pos):
    game = BouncyBalls(controller,pos)
    game.run()

if __name__ == '__main__':
    game = BouncyBalls()
    game.run()