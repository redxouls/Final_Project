# Poly-Bridge 
## Introduction
Poly Bridge is a bridge-building simulation-puzzle game, developed by New Zealand-based indie studio Dry Cactus with music by Canadian composer Adrian Talens, where players build bridges for vehicles to cross. Poly Bridge was released for Microsoft Windows on July 12, 2016, iOS on June 13, 2017.Steel, wood, rope, and cable can be combined and used to strengthen a designed bridge. The game is made more difficult with the availability of different building materials of different prices.        **--- excerpted from Wikipedia**
## Rules
1. Players need to create a bridge sturdy enough for cars to walk on it. If any part of the bridge breaks, the bridge will collapse.
2. Winning condition: Cars can safely get to the right side, with the bridge remaining intact. 
3. Once you click the start button, players will be enable to select their map.
4. There are three maps for players to choose, and each map has different obstacles.
5. After choosing the map, players will get into the game screen, and they can start building their bridges by either right clicking or left clicking to create their own structures.
6. The total number of road trusses and wood trusses is limited, players can see how many available trusses at the top-right corner.
7. Notice that at the top-left corner, there are some words that describe the modes and states that the players are in.
8. In road mode, the trusses that players create are black, and cars can walk on them.
9. In wood mode, the trusses that players create are brown. They are created to enhance the structure, and cars cannot walk on them.
10. In stop state, the bridge will not have any displacement while cars walking on it.
11. In running state, the bridge will be able to have displacement and may even collapse.



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisite

Things you need to install beforehand and how to install them
```
Python3 
pip install pygame
pip install anastruct
pip install vpython
pip install pymunk
```
Enter this in your termianl to download the game
```git clone https://github.com/redxouls/Final_Project.git```

Or go to the [website](https://github.com/redxouls/Final_Project.git) tand find the button clone or download
### Executing
1. After the installation, you have to keep all files in the same folder ( including `main.py`, `Structure.py`, `Controller.py`, `Car.py`, `Truss.py`,`Node.py`, `Bio.py and file for loading test).
2. *If you have a input file to load existing pattern, also keep the files in the same folder(./)
3. To start the game, execute `main.py`
* Make sure you execute it in the same directory with image folder
## Instuctions
![Game Screen](https://i.imgur.com/Z0piusu.png)

### Step1: Choose a material to build the bridge (wood/road), wood is for support while car can only drive on the road.
### Step2: Use the mouse along the keyboard to edit and build the bridge(left/right cliick) 
### Step3: Press "shift" to start trial and press "space" to release the car
### Step4: If you losses, you can press "4" to recover your bridge
### Step5: If you want to save the creation press "s" and enter a filename
### Step6: If want to load a saved creation you can press "f" and enter the filename (Only creartion from same map)
----
### Game Control Button:

#### `1. START! button:` Start the Game operation 
#### `2. EXIT GAME button:` End the Game
#### `3. HELP button:` Get instructions
#### `4. RESUME Button:` Resume the game
#### `5. MENU Button:` Return to the menu

### Game Control Button (Keyboard):
#### * Chossing Building Materials
#### `1. "1" :` To set up "Road" Truss(which is black)
#### `2. "2" :` To set up "Wood" Truss(which is brown)
#### * Runing Trial
#### `3. "4" :` After each test press it to recover
#### `4. "Shiift" :` To stop or run the test
#### `5. "Space" :` Put a car onto the field
#### * Modification of the bridge
#### `6. "d" :` Press and Hold it as you grag to select an area with right click 
#### `7. "e" :` Cancel the selection 
#### `8. "Backspace" :` Delete trusses and nodes you just select 
#### `9. "a" :` Move a node within range
#### * Output and Load files
#### `10. "s" :` Save your magnificent work into a file by entering filename in the terminal
#### `11. "l" :` Load the creation you saved by entering filename in the terminal
#### Note: Only creation from same map can be loaded

### Mouse Control :
#### Left click : (1) if you press once, a node is created  (2) if you hold it and link to other place, a truss is created
#### Rigth click : mostly the same as Left click, but you can create trusses without linking to any existing nodes

## Part I: Class Explan
### Controller:
#### * Usage: It controls and manipulate other classes by calling their class methods and gather all information.response to every mouse control and keyborad when `main.py` calls.

#### * Function: Including 4 main types (1) interface changing  (2) screen update (3)add new object and store them in according attribute (4) modify or delete existing objects 
### Structure
#### * Usage: All trusses information are stored here; Every controller handle a struture, and a new one every map or new game

#### * Function: Deal with (1) bridge defromatioin analyze (2) collapse judging (3)ouput structure (4) load strucuture
### Truss
#### * Usage: Record the connection between two nodes which change with the nodes object's position

#### * Function: (1) length  (2) draw 
### Node
#### * Usage: Record the position of a single node

#### * Function: (1) change position  (2) draw (3)check if clicked
### Car
#### * Usage: During the trial the car interact with truss thus change nodes' position and cause deformation

#### * Function: (1) draw the car (2) transform road to pymunk object that the car can move on
### Ball
#### * Usage: When Car is moving Ball keep track of its physics parameter and detect which truss to load on 

#### * Function: (1)calculate the distance between the nearest truss and its center of mass (2)detect collision with truss to apply load on structure

### Bio
#### * Usage: When the bridge collapse, it shows a short animation of collapsing bidge

#### * Function: (1)add object to fall (2) collide with ground and each other

## Part II: Function Explaination
* Note: some program below is omitted or simplified to be more readable


### `main.py`
```python=
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

k = input("File name:")
x = int(input("width"))
y = int(input("height"))
initial_pos=[int(input("Initial x:")),int(input("Initial y:"))]
csize = int(input("cell size"))
root,sub1,sub2,,reset,cell1,cell2
```

| Variables|Type| Usage |
| :--------: | :--------: | -------- |
|main_controller|Controller|Control all other objects|
|main_controller.structure|Structure|Store all trusses and nodes|
|bg,screen|pygame object|Pygame Object to control the Gaming Screen|
|clock|pygame object|Pygame Object to Control the screen's update speed |

### `Controller.py`
```python=
import sys, pygame, time, copy, os, json
import numpy as np
from pygame.locals import *
from anastruct import SystemElements
from vpython import *
from Ball import *
from Node import *
from Truss import *
from Bio import *
from Structure import *
class Controller():
    def __init__(self,structure,screen):
        self.win = False
        self.di = os.getcwd()
        self.dir = os.path.join(self.di,'images')
        path10 = os.path.join(self.dir,'esc_bg2.png')
        self.background_size = (1280,960)
        self.origin_game_bg = pygame.image.load(path10).convert_alpha()
        self.game_bg = pygame.transform.scale(self.origin_game_bg,self.background_size)
        #
        self.structure = structure
        self.screen = screen
        self.balls = []
        self.t = 0
```
***Function:*** Import needed modules and declare numerous variables for mouse control, mode switching, game status, temporarily saved coordinate.

***Return:*** None
```python=
def findnode(self,mpos):
    structure = self.structure
    self.reltruss = []
    nid = -1
    screen,nodes,click,trusses = structure.screen, structure.nodes, self.click, structure.trusses
    for i in range(len(nodes)):
        check = nodes[i]
        if check.clicked(mpos):
            nid=i
            break
    for tru in trusses:
        if tru.nodeA == nodes[nid] or tru.nodeB == nodes[nid]:
            self.reltruss.append(tru)
    return nid
```
***Function:*** Given the mouse position,it finds the node id that is clicked by the mouse

***Return:*** It will return the node id,if nothing is clicked,it returns -1. 
```python=
def mvnode(self,mpos):
    structure = self.structure
    screen,nodes,click,trusses = structure.screen, structure.nodes, self.click, structure.trusses
    npos = vector(mpos[0],mpos[1],0)
    for tru in self.reltruss:
        if mag(npos-tru.nodeA.pos) > self.tmpc[2] or mag(npos-tru.nodeB.pos) > self.tmpc[2]:
            return
    nodes[self.altednode].pos = npos
```
***Function:*** Given the mouse position,the function determines whether the node movement is legal by checking the truss length,if so,the node will move. 

***Return:*** None

```python=
def delarea(self):
    x1=self.dltcod[0][0]
    x2=self.dltcod[1][0]
    y1=self.dltcod[0][1]
    y2=self.dltcod[1][1]
    structure = self.structure
    ...
    omitted
    ...
```
***Function:*** It uses parametric equation to determine if the rectangle pulled out by the mouse includes the trusses or the node.If so,we add them into dltnode and dlttruss. 

***Return:*** None
```python=
def initial_platform(self,mapid):
    structure = self.structure
    if mapid == 1:
        self.car_position = vector(60,650,0)
        structure.truss_limit = 25
        left_nodeA = structure.add_node(0,700)
        left_nodeB = structure.add_node(200,700)
        structure.add_truss(left_nodeA,left_nodeB,0)
    if mapid == 2:
        self.car_position = vector(60,150,0)
        structure.truss_limit = 25
        return
    if mapid ==3:
        left_nodeA = structure.add_node(0,700)
        left_nodeB = structure.add_node(200,700)
        structure.add_truss(left_nodeA,left_nodeB,0)
        return
```
***Function:*** Given map id,we create different scenarios for each map.Note that the third map contains obstacles 

***Return:*** None
```python=
def recov(self):
    self.dltnode=[]
    self.dlttruss=[]
```
***Function:*** Clear the node to delete and truss to delete. 

***Return:*** None
```python=
def clear(self):
    structure = self.structure 
    for nd in self.dltnode:
        structure.nodes.remove(nd)
    for tru in self.dlttruss:
        structure.trusses.remove(tru)
        if tru in self.structure.roadtrusses:
            self.structure.roadtrusses.remove(tru)
    self.recov()
```
***Function:*** Eliminate the trusses and nodes that are selected. 

***Return:*** None

```python=
def game_start_interface(self):
def esc_interface(self):
def choose_map_interface(self):
def help_interface(self):
```
***Function:*** Create different interfaces by using functions in pygame module such like blit, render, load, font.

***Return:*** None
```python=
def click_start_button(self,downcod):
def click_exit_button(self,downcod):
def click_esc_resume_button(self,downcod):
def click_esc_restart_button(self,downcod):
def click_esc_exit_button(self,downcod):
def click_map1_button(self,downcod):
def click_map2_button(self,downcod):
def click_map3_button(self,downcod):
def click_help(self,downcod):
```
***Function:*** Determing whether the mouse clicked on these buttons or not.

***Return:*** Boolean Value



### `Car.py`
```python=
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
```
***Function:*** Initializing car object with given `controller` , `pos`.After loading the structure and the car position, we create a space and put all trusses into a space accordingly. 

***Return:*** None
```python=
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
    
    mass = 150
    size = (50,30)
    moment = pymunk.moment_for_box(mass, size)
    chassi_b = pymunk.Body(mass, moment)
    chassi_s = pymunk.Poly.create_box(chassi_b, size)
    self._space.add(chassi_b, chassi_s)


    wheel1_b.position = pos - (55,0)


    self._space.add(
        pymunk.PinJoint(wheel1_b, chassi_b, (0,0), (-25,-15)),
        
        )
        
    speed = -20
    self._space.add(
    pymunk.SimpleMotor(wheel1_b, chassi_b, speed),
    pymunk.SimpleMotor(wheel2_b, chassi_b, speed)
    )
```
***Function:*** We first create two circles,we designate their masses and radius.Then we create a box and designate its size and mass.Later we add them to space,and use pin joints to connect them.Finally,we give the car its speed and angular velocity by SimpleMotor.(This function partially references the pymunk documentaion)

***Return:*** None. 
```python=
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
    ...
    omitted
    ...
    self._space.add(static_lines)
```
***Function:*** It collects the current trusses,and then remove the old trusses.Then,we add static lines to the space and give them elasticity and friction.

***Return:*** None
```python=
def _update_balls(self):
    """
    Create/remove balls as necessary. Call once per frame only.
    :return: None
    """
    self._create_ball(self.pos)
```
***Function:*** It creates a car.

***Return:*** None
### `Truss.py`
```python=
def __init__(self,nodeA=None,nodeB=None,screen=None,*,pos=None,axis=None,radius=None):
    self.nodeA = nodeA
    self.nodeB = nodeB
    if self.nodeA!= None and self.nodeB != None:
        self.oril = mag(nodeA.pos-nodeB.pos)
    self.screen = screen
    self.maxforce = 100
    self.collided = False
    self.pos = pos
    self.axis = axis
    self.radius = radius
    self.collapse = False
```
***Function:*** Initialize the truss with given two nodes

***Return:*** None
```python=
def draw_Truss(self,todel):
    screen = self.screen
    if todel:
        pygame.draw.line(self.screen,(230,230,230), self.nodeA.to_int(), self.nodeB.to_int(), 17)
    else:
        pygame.draw.line(self.screen,(204,102,0), self.nodeA.to_int(), self.nodeB.to_int(), 17)
```
***Function:*** It draws supportive trusses with different colors based on the given boolean variable 'todel',which indicates whether the truss is to be deleted

***Return:*** None
```python=
def draw_marked_Truss(self,todel):
    screen = self.screen
    if todel:
        pygame.draw.line(self.screen,(230,230,230), self.nodeA.to_int(), self.nodeB.to_int(), 17)
    else:
        pygame.draw.line(self.screen,(0,0,0), self.nodeA.to_int(), self.nodeB.to_int(), 17) 
```
***Function:*** It draws road trusses with different colors based on the given boolean variable 'todel',which indicates whether the truss is to be deleted

***Return:*** None
```python=
def draw_obtruss(self):    
    screen = self.screen
    pygame.draw.line(self.screen,(30,170,30), self.nodeA.to_int(), self.nodeB.to_int(), 17) 
```
***Function:*** It draws obstructive trusses.

***Return:*** None
```python=
def length(self):
    return mag(self.nodeA.pos-self.nodeB.pos)
```
***Function:*** It calculates the length of the truss.

***Return:*** length of the truss
```python=
def truss_touch(self,other):
    px1 = (self.nodeA.pos.x,self.nodeB.pos.x-self.nodeA.pos.x)
    py1 = (self.nodeA.pos.y,self.nodeB.pos.y-self.nodeA.pos.y)
    px2 = (other.nodeA.pos.x,other.nodeB.pos.x-other.nodeA.pos.x)
    py2 = (other.nodeA.pos.y,other.nodeB.pos.y-other.nodeA.pos.y)
    ...
    omitted
    ...
    delta = (a1*b2-a2*b1)
    if delta == 0:
        return True
    deltax = (c1*b2-c2*b1)
    deltay = (a1*c2-a2*c1)
    if 0 <= deltax/delta <= 1 and 0 <= deltay/delta <= 1:
        return True
    return False
```
***Function:*** It takes in two trusses and see if they intersect.

***Return:*** Whether two trusses intersect
### `Node.py`
```python=
def __init__(self,x=0,y =0,screen=None,*,pos=None,radius=None):
    if pos == None:
        self.pos = vector(x,y,0)
    else:
        self.pos = pos
    self.radius = 15
    self.maxforce = 0.000000002
    self.screen = screen
```
***Function:*** Initialize the node with given position

***Return:*** None
```python=
def draw_node(self,todel):
    screen = self.screen
    if todel:
        pygame.draw.circle(screen, (230, 230, 230), self.to_int(), self.radius, 0)
    else:
        pygame.draw.circle(screen, (96, 96, 96), self.to_int(), self.radius, 0)
    return 
```
***Function:*** It draws nodes with different colors based on the given boolean variable 'todel',which indicates whether the truss is to be deleted

***Return:*** None
```python=
def draw_obnode(self):
    screen = self.screen
    pygame.draw.circle(screen, (30, 170, 30), self.to_int(), self.radius, 0)
    return
```
***Function:*** It draws obstructive nodes

***Return:*** None
```python=
def clicked(self,mouse_pos):
    distance = ((self.pos.x-mouse_pos[0])**2+(self.pos.y-mouse_pos[1])**2)**0.5
    if distance <= self.radius+10:
        return True
    else:
        return False
```
***Function:*** Determines whether the node is clicked by checking if 'mouse_pos' is in the circle of the node 

***Return:*** whether the node is clicked
```python=
def to_int(self):
    return int(self.pos.x), int(self.pos.y)
```
***Function:*** Since pygame uses integer coordinates,the function transfers float coordinates into integers

***Return:*** integer coordinate tuple
### `Structure.py`
```python=
def __init__(self,screen):
    self.truss_limit = 25
    self.trusses = []
    self.nodes = []
    self.click = False
    self.lastc = 0
    self.screen = screen
    self.t = 0
    self.Bios = []
    self.loadid = []
    self.roadtrusses=[]
    self.collapse = False
    self.dlt=False
    self.dltcod=[(0,0),(0,0)]
    self.dltnode=[]
    self.dlttruss=[]
    self.tmpc=[False,(0,0),120]
    self.unstable = False
    self.tempnodespos = []
    self.obtruss = []
    self.obnode = []
```
***Function:*** Initialize our bridge structure,containing all information needed of the structure

***Return:*** None
```python=
def add_node(self,x,y):
    if len(self.trusses)> self.truss_limit +1 :
        return
    new_node = Node(x=int(x),y=int(y),screen=self.screen)
    self.nodes.append(new_node)
    return new_node
```
***Function:*** It adds nodes to list 'self.nodes' with given position

***Return:*** the new node that is created
```python=
def add_obtruss(self,nodeA,nodeB):
    new_truss = Truss(nodeA,nodeB,self.screen)
    self.obtruss.append(new_truss)
    return new_truss
```
***Function:*** It adds trusses to list 'self.trusses' with given nodes

***Return:*** the new truss that is created
```python=
def add_obtruss(self,nodeA,nodeB):
    new_truss = Truss(nodeA,nodeB,self.screen)
    self.obtruss.append(new_truss)
    return new_truss
```
***Function:*** Similar to the 'add_truss' function,it adds obstructive trusses to list'obtruss'

***Return:*** the new obstructive truss that is created
```python=
def add_obnode(self,x,y):
    new_node = Node(x=int(x),y=int(y),screen=self.screen)
    self.obnode.append(new_node)
    return new_node
```
***Function:*** Similar to the 'add_node' function,it adds obstructive nodes to list'obnode'

***Return:*** the new obstructive node created
```python=
def set_orilen(self):
    for truss in self.trusses:
        truss.oril = truss.length()
    for truss in self.roadtrusses:
        truss.oril = truss.length()
```
***Function:*** Set up the original length for each truss in order to facilitate the calculation of the collapse of truss 

***Return:*** None

### `Ball.py`
```python=
class Ball:
    def __init__(self,screen,label,pos=vector(0,0,0)):
        self.label = label
        self.screen = screen
        self.radius = 10
        self.g = 9.8
        self.efficient = 0.01
        self.colleffi = 0.8
        self.power = 40.0
        self.v = vector(0,0,0)
        self.pos = pos
        self.a = vector(0,self.g,0)
        self.free = True
```
***Function:*** Initiallize several physics parameters to track the movement of the two wheels of the car.

***Return:*** None
```python=
    def distance(self,*,node=None,truss=None):
        if node != None:
            return (self.pos[0]-node.cod[0]**2+(self.pos[1]-node.cod[1]**2)**0.5)
        if truss != None:
            return
```
***Function:*** With given  truss or node, it calculate the shortest distance between

***Return:*** the distance calulated (float)
```python=
    def nearest(self,structure):
        for i in range(len(structure.roadtrusses)):
            truss = structure.roadtrusses[i] 
            if truss.collapse:
                continue
            if self.pos.x>=truss.nodeA.pos.x and self.pos.x<truss.nodeB.pos.x:
                return i
            if self.pos.x<truss.nodeA.pos.x and self.pos.x>=truss.nodeB.pos.x:
                return i
```
***Function:*** It search the closest truss in roadtrusses and return the index of the neareset one

***Return:*** index of the nearest truss(int)

```python=
    def ground_distance(self,structure):
        if self.nearest(structure) == None:
            return
        ground = structure.roadtrusses[self.nearest(structure)]
        v1 = self.pos - vector(ground.nodeA.pos.x,ground.nodeA.pos.y,0)
        v2 = vector(ground.nodeB.pos.x,ground.nodeB.pos.y,0) - vector(ground.nodeA.pos.x,ground.nodeA.pos.y,0)
        theta = acos(v1.dot(v2)/(v1.mag*v2.mag))
        distance = v1.mag*sin(theta)
        return distance
```
***Function:*** Utilizing the two function distance and nearest to calculate the distance between the car's wheel and the roadtrusses 

***Return:*** distance(float)
### `Bio.py`


```python=
    
class Bio():
    def __init__(self,*,pos=None, axis=None,screen=None,d=2.5*20,nodeA=None,nodeB=None):
        if nodeA != None and nodeB!= None: 
            self.O = nodeA
            self.C = nodeB
            axis = nodeA.pos-nodeB.pos
            d = axis.mag
        else:
            self.O = Node(pos=pos, radius=20)
            self.C = Node(pos=pos+axis, radius=20)
        self.bond = Truss(pos=pos, axis=axis, radius=20/2.0)
        self.O.m = 20
        self.C.m = 20
        self.O.v = vector(0, 0, 0)
        self.C.v = vector(0, 0, 0)
        self.d = d
        self.dt = 0.1
        self.bond.k = 500.0
        self.screen = screen
        self.b =  0.05 * sqrt(self.bond.k*self.O.m)
        self.gravity = vector(0,9.8,0)
```
***Function:*** Initiallize physics parameters for falling trusses, and take advantage of both node and truss two class

***Return:*** None
```python=

    def bond_force_on_O(self):        # return bond force acted on the O atom
        return self.bond.k * (mag(self.bond.axis)-self.d) * norm(self.bond.axis) - self.b*(self.O.v-(self.O.v+self.C.v)/2)
```
***Function:*** It define the way the two nodes connected to each others, and calculate the force accordingly

***Return:*** force to keep this to nodes together(float)
```python=
    def time_lapse(self):         # by bond's force, calculate a, v and pos of C and O, and bond's pos and axis after dt 
        dt = self.dt
        self.C.a = -self.bond_force_on_O() / self.C.m +  self.gravity  # 
        self.O.a = self.bond_force_on_O() / self.O.m + self.gravity # 
        self.C.v += self.C.a * dt
        self.O.v += self.O.a * dt
        self.C.pos += self.C.v * dt
        self.O.pos += self.O.v * dt
        self.bond.axis = self.C.pos - self.O.pos
        self.bond.pos = self.O.pos
```
***Function:*** The trusses move over time like a physics simulation, and this function update these objects position, velocity, and accerlation

***Return:*** None
```python=
    def ground_collision(self):
        if self.O.pos.y > 900:
            self.O.v.y*= -1
        if self.C.pos.y > 900:
            self.C.v.y*= -1
```
***Function:*** If the trusses and nodes fall onto the ground, the ball collide with the ground.

***Return:*** None
```python=
    def collision(a1, a2):
        v1prime = a1.v - 2 * a2.m/(a1.m+a2.m) *(a1.pos-a2.pos) * dot (a1.v-a2.v, a1.pos-a2.pos) / mag(a1.pos-a2.pos)**2
        v2prime = a2.v - 2 * a1.m/(a1.m+a2.m) *(a2.pos-a1.pos) * dot (a2.v-a1.v, a2.pos-a1.pos) / mag(a2.pos-a1.pos)**2
        return v1prime, v2prime
```
***Function:*** This function takes in two nodes and handle collision between these two nodes

***Return:*** None
```python=
    def system_check_collision(self,COs):
        N = len(COs)
        for i in range(N-1):        
            for j in range(i+1,N):  
                if (COs[i].C.pos-COs[j].C.pos).mag<=2*COs[i].C.radius and dot(COs[i].C.pos-COs[j].C.pos,COs[i].C.v-COs[j].C.v)<0:
                    COs[i].C.v, COs[j].C.v = Bio.collision(COs[i].C,COs[j].C)
                if (COs[i].C.pos-COs[j].O.pos).mag<=2*COs[i].C.radius and dot(COs[i].C.pos-COs[j].O.pos,COs[i].C.v-COs[j].O.v)<0:
                    COs[i].C.v, COs[j].O.v = Bio.collision(COs[i].C,COs[j].O)
                if (COs[i].O.pos-COs[j].C.pos).mag<=2*COs[i].C.radius and dot(COs[i].O.pos-COs[j].C.pos,COs[i].O.v-COs[j].C.v)<0:
                    COs[i].O.v, COs[j].C.v = Bio.collision(COs[i].O,COs[j].C)
                if (COs[i].O.pos-COs[j].O.pos).mag<=2*COs[i].C.radius and dot(COs[i].O.pos-COs[j].O.pos,COs[i].O.v-COs[j].O.v)<0:
                    COs[i].O.v, COs[j].O.v = Bio.collision(COs[i].O,COs[j].O)
```
***Function:*** This function check if any nodes collide into one another and call collision function to change their speed

***Return:*** None
```python=
    def draw_Truss(self,screen):
        pygame.draw.line(screen,(204,102,0), self.to_int(1), self.to_int(2), 17)

    def draw_node(self,screen):
        pygame.draw.circle(screen, (0, 127, 255), [int(self.O.pos.x), int(self.O.pos.y)], self.C.radius, 0)
        pygame.draw.circle(screen, (0, 127, 255), [int(self.C.pos.x), int(self.C.pos.y)], self.C.radius, 0)
        return
```
***Function:*** Draw objects onto pygame screen
***Return:*** None
```python=
    def to_int(self, num):
        if num ==1:
            return [int(self.C.pos.x),int(self.C.pos.y)] 
        if num ==2:
            return [int(self.O.pos.x),int(self.O.pos.y)]
```
***Function:*** Convert vpython vector to two integer coordinate for pygame screen to draw objects
***Return:*** coodinate of two objects(list)

## Short Tutorial
* You can try to load photes
![](https://i.imgur.com/59pc88o.jpg)
![](https://i.imgur.com/eyl4CtU.jpg)
![](https://i.imgur.com/0QEYeWx.jpg)
/iTo keep the structure stable,we construct the trusses in a triangular form.Also,we build it like an arc so that it undertakes more weight.Surely,there are no standard answers for games,so just utilize your creativity and have fun.a
* For example video.Here's the [link](https://drive.google.com/file/d/1fbx8Q-HZ9SAvJcgNmakLJyEbfEgf52qX/view)

### See more information on https://github.com/redxouls/Final_Project

## Built With

* [Anaconda](https://www.anaconda.com/) - The environment used
* [pygame](https://www.pygame.org/news) - module used to visualize the game
* [anastruct](https://github.com/ritchie46/anaStruct) - For Bridge deformation and analyze
* [pymunk](http://www.pymunk.org/en/latest/) - For the car's movement and collision detection
* [vpython](https://vpython.org/) - Using vectors and physics tools

## Contributions


### 1. 陳宏恩
* ***In charge of the main structure of this game and Final integration of different classes***
* ***Interaction between Objects(Truss&Ball&Car&Structure)***
* ***Coordinate between differnet modules(Anastruct ananlyzing, pymunk segmentaion loading and the collapse animation of the bridge)***
* ***Structure Ouput and Load***
* Captain Teemo on duty
* Carry the whole team
* GPA 4.301
* Cotton picking master
* King of Africa
* Final exam got 91 points
![Sleeping soundly](https://i.imgur.com/UZyT5A0.jpg)
### 2. 翁茂齊
* ***In charge of screen updating and all gaming interfaces***
* ***Find picture materials and Master of 小畫家***
* ***Bridge collapse judging and Game status Controlling***
* ***Lots of pygame object dispay*** 
* Beated Mason on Calculus quiz by 20 points
* Loose sphincter?!
* Guitar God
* Violin God
* Master of tkinter
![Mochi](https://i.imgur.com/PVeFlkc.jpg)
### 3. 汪昊新 
* ***In charge of mouse controll(deleting/moving trusses and nodes) and keyboard controll***
* ***bridge edition and Car movement (pymunk)***
* ***Obstacles interaction handling***
* ***Deal with complicated physic stuff and is a math genius***
* The One and only, who think the Final Exam is a piece of cake and leave two hours earlier before the due time
* master of dynamic bullshitting
![handsome young man](https://i.imgur.com/kL4iQ8O.jpg)
