from tkinter import *
from random import randrange
from math import ceil, floor
from typing import List
import copy
from time import sleep

# declare default constants
debug = False

# set up window
window = Tk()
window.title('Karel the Robot')
window.minsize(height=800, width=800)
window.config(background="light blue")

# helper functions
def isEven(n: int) -> bool:
    'determine its parity'
    return n % 2 == 0

def timing(speed):
    if speed == 0:
        sleep(1)
    elif speed ==1:
        sleep(.3)

def post_message(msg: str):
    print(msg)
    quit()

def makeworld(wide: int, high: int) -> List[List]:
    'build a list of lists to represent the world with True meaning there is a wall and False meaning there is not one to begin with, "" is unused, 0 means no beepers present in a cell'
    newworld = []
    for y in range(2*high + 1):
        if y == 0 or y == 2*height : #row with just horizontal walls
            row = ["", True]*wide
        elif isEven(y):           #row with just horizontal walls
            row = ["", False]*wide
        else:                     #row with vertical walls and Karel spots
            row = [True]+[0, False]*(wide - 1) + [0, True]
        newworld += [row]
    return newworld

# define world class
class Robot:

    def __init__(self, aframe: Canvas, heading: int, xpos: int, ypos: int, speed: int = 0):
        self.xpos = 0
        self.ypos = ypos
        self.wide = xpos
        self.high = ypos
        self.heading = heading
        self.aframe = aframe
        self.speed = 0
        self.status = [heading, xpos, ypos] # first value is heading 0 = East, 1 = South, 2 = West, 3 = North        
        self.draw()

    def draw(self):
        xpixel = 40*self.xpos-20  # find pixel coordinates of the upperleft corner of Karel's body
        ypixel = 40*self.ypos-20
        self.aframe.create_rectangle(xpixel, ypixel, xpixel+20, ypixel+20, outline = "darkblue", fill = '')
        if self.heading == 0: #facing East
            self.aframe.create_rectangle(xpixel+4, ypixel-6, xpixel+16, ypixel-2, outline = "darkblue", fill = '')
            self.aframe.create_line(xpixel+10, ypixel, xpixel+10, ypixel-2, width = 5, fill = "darkblue")
            self.aframe.create_line(xpixel+10, ypixel+20, xpixel+10, ypixel+24, width = 3, fill = "darkblue")
            self.aframe.create_line(xpixel+8, ypixel+24, xpixel+15, ypixel+24, width = 3, fill = "darkblue")
        elif self.heading == 1: #facing South
            self.aframe.create_rectangle(xpixel+22, ypixel+4, xpixel+26, ypixel+16, outline = "darkblue", fill = '')
            self.aframe.create_line(xpixel+20, ypixel+10, xpixel+22, ypixel+10, width = 5, fill = "darkblue")
            self.aframe.create_line(xpixel, ypixel+10, xpixel-4, ypixel+10, width = 3, fill = "darkblue")
            self.aframe.create_line(xpixel-4, ypixel+10, xpixel-4, ypixel+17, width = 3, fill = "darkblue")
        elif self.heading == 2: #facing West
            self.aframe.create_rectangle(xpixel+4, ypixel+26, xpixel+16, ypixel+22, outline = "darkblue", fill = '')
            self.aframe.create_line(xpixel+10, ypixel+20, xpixel+10, ypixel+22, width = 5, fill = "darkblue")
            self.aframe.create_line(xpixel+10, ypixel, xpixel+10, ypixel-4, width = 3, fill = "darkblue")
            self.aframe.create_line(xpixel+5, ypixel-4, xpixel+12, ypixel-4, width = 3, fill = "darkblue")
        else: #heading == 3, facing North
            self.aframe.create_rectangle(xpixel-2, ypixel+4, xpixel-6, ypixel+10, outline = "darkblue", fill = '')
            self.aframe.create_line(xpixel, ypixel+10, xpixel-2, ypixel+10, width = 5, fill = "darkblue")
            self.aframe.create_line(xpixel+20, ypixel+10, xpixel+24, ypixel+10, width = 3, fill = "darkblue")
            self.aframe.create_line(xpixel+24, ypixel+10, xpixel+24, ypixel+3, width = 3, fill = "darkblue")

    def erase(self):
        xpixel = 40*self.xpos-20  # find pixel coordinates of the upperleft corner of Karel's body
        ypixel = 40*self.ypos-20
        self.aframe.create_rectangle(xpixel, ypixel-3, xpixel+20, ypixel+24, outline = "white", width = 8, fill = '')

    def set_xpos(self, xpos):
        self.xpos = xpos
    
    def set_yloc(self, ypos):
        self.ypos = ypos

    def set_heading(self, heading):
        self.erase()
        self.heading = heading     
        self.draw()
        timing(self.speed)

    def right(self):
        self.erase()
        self.heading = (self.heading + 1) % 4
        self.draw()
        timing(self.speed)

    def left(self):
        self.erase()
        self.heading = (self.heading - 1) % 4
        self.draw()
        timing(self.speed)
  
    def move(self):  # add check for when the wall is gone -- that changes the message.
        if self.heading == 0: # move east if possible
            if self.xpos < self.wide:
                self.xpos += 1
            else:
                post_message("Karel has crashed into a wall!")
        elif self.heading == 2: # move west if possible
            if self.xpos > 1:
                self.xpos -= 1
            else:
                post_message("Karel has crashed into a wall!")
        elif self.heading == 1: # move south if possible
            if self.ypos < self.height():
                self.ypos += 1
            else:
                post_message("Karel has crashed into a wall!")
        elif self.heading == 3: # move north if possible
            if self.ypos > 1:
                self.ypos -= 1
            else:
                post_message("Karel has crashed into a wall!")

# define world class
class World:

    def __init__(self, aframe: Canvas, wide: int=6, high: int=6):
        self._wide = wide
        self.high = height
        self.aframe = aframe
        self.world = makeworld(wide, high)
        self.draw_world()
        self.aframe.bind("<Button-1>", self.follow)

    def draw_world(self):
        'Draw the grid for Karel'
        self.aframe.delete('all')
        gridwidth = len(self.world[0]) // 2
        gridheight = len(self.world) // 2
        for y in range(gridheight):
            for x in range(gridwidth):
                self.aframe.create_rectangle(10+ 40*x, 10+40*y, 50+40*x, 50+40*y, outline = "LightGray")
        self.aframe.create_rectangle(10, 10, 50+40*x, 50+40*y, outline = "black", width = 3)
    
    def displayBeeperCount(self, x, y, numBeepers):
        'Display the number of beepers in that cell (or erase if 0)'
        if numBeepers > 0:
            self.aframe.create_oval(40*x-17, 40*y-17, 40*x-3, 40*y-3, fill="darkBlue")
            self.aframe.create_text(40*x-9, 40*y-10, text=numBeepers, fill="white", font=('Helvetica 10 bold'))
        else: # erase marker when no beepers are present
            self.aframe.create_oval(40*x-18, 40*y-18, 40*x-2, 40*y-2, fill="white", outline = "white")

    # Input: location of a mouse click
    def follow(self, event):
        'Determine what part of the grid was clicked and update wall and beeper status accordingly'
        if event.x >= 10 and event.y >=10 and event.x <= 10 + 40*self.width and event.y <= 10 + 40*self.height:
            xcor = (event.x - 10) % 40
            ycor = (event.y - 10) % 40
            if (ycor >= 8) and (ycor <= 32) and (xcor >= 8) and (xcor <= 32):  # in the center of a grid square
                xloc = ceil((event.x - 10) / 40)   # which cell
                yloc = ceil((event.y - 10) / 40)
                if debug:
                    print("Beeper", xloc, yloc)
                self.world[yloc*2][xloc*2-1] += 1
                self.world[yloc*2][xloc*2-1] = self.world[yloc*2][xloc*2-1] % 4  # cycle through 0 - 4 on clicks
                self.displayBeeperCount(xloc, yloc, self.world[yloc*2][xloc*2-1])
            elif (abs(ycor - xcor) <= 6) or (abs(ycor - xcor) >= 34):  # near a corner so we don't know which to count line
                if debug:
                    print("null") 
            elif ((ycor <= 8) or (ycor >= 32)) and not ((xcor <= 8) or (xcor >= 32)) :  # near a horizontal line
                xloc = ceil((event.x - 10) / 40)   # which row
                yloc = round((event.y - 10) / 40)
                if debug:
                    print("row: ", xloc, yloc)
                self.world[yloc*2][xloc] = not self.world[yloc*2][xloc]
                if self.world[yloc*2][xloc]: # draw a wall
                    self.aframe.create_line(10 + 40*(xloc-1), 10+40*yloc, 50+40*(xloc-1), 10+40*yloc, fill = "black", width = 3)
                else: # erase a wall
                    self.aframe.create_line(10 + 40*(xloc-1), 10+40*yloc, 50+40*(xloc-1), 10+40*yloc, fill = "white", width = 3)           
                    self.aframe.create_line(10 + 40*(xloc-1), 10+40*yloc, 50+40*(xloc-1), 10+40*yloc, fill = "LightGray", width = 1)           
            elif (xcor <= 8) or (xcor >= 32) and not ((ycor <= 8) or (ycor >= 32)):  # near a vertical line
                xloc = round((event.x - 10) / 40)   # which column
                yloc = ceil((event.y - 10) / 40)
                if debug:
                    print("column: ", xloc, yloc)
                self.world[yloc*2-1][xloc*2] = not self.world[yloc*2-1][xloc*2]
                if self.world[yloc*2-1][xloc*2]: # draw a wall
                    self.aframe.create_line(10 + 40*xloc, 10+40*(yloc-1), 10+40*xloc, 50+40*(yloc-1), fill = "black", width = 3)
                else: # erase a wall
                    self.aframe.create_line(10 + 40*xloc, 10+40*(yloc-1), 10+40*xloc, 50+40*(yloc-1), fill = "white", width = 3)           
                    self.aframe.create_line(10 + 40*xloc, 10+40*(yloc-1), 10+40*xloc, 50+40*(yloc-1), fill = "LightGray", width = 1)           
            else:
                if debug:
                    print("null")  
                    
    @property
    def wide(self):
        return self._wide
    
    @width.setter
    def wide(self, wide: int):
        self._wide = wide
        self.world = makeworld(self._wide, self._high)
        self.draw_world()
    
    def set_wide(self, wide):
        self.wide = wide
    
    def set_height(self, height):
        self.high = high

    def hurdles(self):
        'set up challenge'

    def mountain(self):
        'set up challenge'

    def cleanup(self):
        'set up challenge'

    def complete_box(self):
        'set up challenge'

    def find_double(self):
        'set up challenge'

    def maze(self):
        'set up challenge'

    def sort(self):
        'set up challenge'

    def blockade(self):
        'set up challenge'

    def binary(self):
        'set up challenge'

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, high: int):
        self._high = high
        self.world = makeworld(self._wide, self._high)
        self.draw_world()

def mysolution(karel: Robot):
    karel.move()

# main thread
def setup():
    aframe = Canvas(window, width = 800, height = 900)  # create a region for drawing
    aframe.pack(side = BOTTOM)
    world = World(aframe)
    karel = Robot(aframe, 0, 1, world.height, world.wide)
    karel.draw()
    
    #set up menus
    menubar = Menu(window)
    window.config(menu=menubar)
    WidthMenu = Menu(menubar)
    WidthMenu.add_command(label="6", command= lambda: world.set_width(6))
    WidthMenu.add_command(label="7", command= lambda: world.set_width(7))
    WidthMenu.add_command(label="8", command= lambda: world.set_width(8))
    WidthMenu.add_command(label="9", command= lambda: world.set_width(9))
    WidthMenu.add_command(label="10", command= lambda: world.set_width(10))
    WidthMenu.add_command(label="11", command= lambda: world.set_width(11))
    WidthMenu.add_command(label="12", command= lambda: world.set_width(12))
    WidthMenu.add_command(label="13", command= lambda: world.set_width(13))
    WidthMenu.add_command(label="14", command= lambda: world.set_width(14))
    WidthMenu.add_command(label="15", command= lambda: world.set_width(15))
    WidthMenu.add_command(label="16", command= lambda: world.set_width(16)) 
    menubar.add_cascade(label="Width", menu=WidthMenu)
    HeightMenu = Menu(menubar)
    HeightMenu.add_command(label="6", command= lambda: world.set_height(6))
    HeightMenu.add_command(label="7", command= lambda: world.set_height(7))
    HeightMenu.add_command(label="8", command= lambda: world.set_height(8))
    HeightMenu.add_command(label="9", command= lambda: world.set_height(9))
    HeightMenu.add_command(label="10", command= lambda: world.set_height(10))
    HeightMenu.add_command(label="11", command= lambda: world.set_height(11))
    HeightMenu.add_command(label="12", command= lambda: world.set_height(12))
    HeightMenu.add_command(label="13", command= lambda: world.set_height(13))
    HeightMenu.add_command(label="14", command= lambda: world.set_height(14))
    HeightMenu.add_command(label="15", command= lambda: world.set_height(15))
    HeightMenu.add_command(label="16", command= lambda: world.set_height(16))   
    menubar.add_cascade(label="Height", menu=HeightMenu)
    ChallengesMenu = Menu(menubar)
    ChallengesMenu.add_command(label="Hurdles", command= world.hurdles)
    ChallengesMenu.add_command(label="Mountain", command= world.mountain)
    ChallengesMenu.add_command(label="CleanUp", command= world.cleanup)
    ChallengesMenu.add_command(label="CompleteBox", command= world.complete_box)
    ChallengesMenu.add_command(label="FindAndDouble", command= world.find_double)
    ChallengesMenu.add_command(label="Maze", command= world.maze)  
    ChallengesMenu.add_command(label="Sort", command= world.sort)
    ChallengesMenu.add_command(label="Blockade", command= world.blockade)
    ChallengesMenu.add_command(label="Binary", command= world.binary)  
    menubar.add_cascade(label="Challenges", menu=ChallengesMenu)
    SpeedMenu = Menu(menubar)
    SpeedMenu.add_command(label="Run", command= lambda: mysolution(karel))
    SpeedMenu.add_command(label="Slow", command= lambda: karel.set_speed(0))
    SpeedMenu.add_command(label="Medium", command= lambda: karel.set_speed(1))
    SpeedMenu.add_command(label="Fast", command= lambda: karel.set_speed(2))
    menubar.add_cascade(label="Speed", menu=SpeedMenu)
    window.mainloop()

setup()