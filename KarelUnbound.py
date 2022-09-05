from tkinter import *
from random import randrange
from math import ceil, floor

debug = True
width = 6 #initial size
height = 6
    
# set up window
window = Tk()
window.title('Karel the Robot')
window.minsize(height=600, width=600)
window.config(background="light blue")

# Input: an integer
# Action: determine its parity
# Output: return true for even, false for not even
def isEven(n):
    return n % 2 == 0

# Input: the width and height of the Karel grid
# Action: build a list of lists to represent the world with True meaning there is a wall and False meaning there is not one to begin with, "" is unused, 0 means no beepers present in a cell
# Output: return the world 
def makeworld(hor, ver):
    world = []
    for y in range(2*ver + 1):
        if y == 0 or y == 2*ver : #row with just horizontal walls
            row = ["", True]*hor
        elif isEven(y):           #row with just horizontal walls
            row = ["", False]*hor
        else:                     #row with vertical walls and Karel spots
            row = [True]+[0, False]*(hor - 1) + [0, True]
        world = world + [row]
    return world

# Input: window, cell affected, beeper count
# Action: display the number of beepers in that cell (or erase if 0)
def displayBeeperCount(aframe, x, y, numBeepers):
    if numBeepers > 0:
        marker = aframe.create_oval(40*x-17, 40*y-17, 40*x-3, 40*y-3, fill="darkBlue")
        count = aframe.create_text(40*x-9, 40*y-10, text=numBeepers, fill="white", font=('Helvetica 10 bold'))
    else: # erase marker when no beepers are present
        marker = aframe.create_oval(40*x-18, 40*y-18, 40*x-2, 40*y-2, fill="white", outline = "white")
        
# Input: location of a mouse click
# Action: determine what part of the grid was clicked and update wall and beeper status accordingly
def follow(event, aframe):  #release object
    #print(event.x, event.y)
    if event.x >= 10 and event.y >=10 and event.x <= 10 + 40*width and event.y <= 10 + 40*height:
        xcor = (event.x - 10) % 40
        ycor = (event.y - 10) % 40
        if (ycor >= 8) and (ycor <= 32) and (xcor >= 8) and (xcor <= 32):  # in the center of a grid square
            xloc = ceil((event.x - 10) / 40)   # which cell
            yloc = ceil((event.y - 10) / 40)
            if debug:
                print("Beeper", xloc, yloc)
            world[yloc*2][xloc*2-1] += 1
            world[yloc*2][xloc*2-1] = world[yloc*2][xloc*2-1] % 4  # cycle through 0 - 4 on clicks
            displayBeeperCount(aframe, xloc, yloc, world[yloc*2][xloc*2-1])
        elif (abs(ycor - xcor) <= 6) or (abs(ycor - xcor) >= 34):  # near a corner so we don't know which to count line
            if debug:
                print("null") 
        elif ((ycor <= 8) or (ycor >= 32)) and not ((xcor <= 8) or (xcor >= 32)) :  # near a horizontal line
            xloc = ceil((event.x - 10) / 40)   # which row
            yloc = round((event.y - 10) / 40)
            if debug:
                print("row: ", xloc, yloc)
            world[yloc*2][xloc] = not world[yloc*2][xloc]
            if world[yloc*2][xloc]:
                awall =aframe.create_line(10 + 40*(xloc-1), 10+40*yloc, 50+40*(xloc-1), 10+40*yloc, fill = "black", width = 3)
            else:
                awall =aframe.create_line(10 + 40*(xloc-1), 10+40*yloc, 50+40*(xloc-1), 10+40*yloc, fill = "white", width = 3)           
                awall =aframe.create_line(10 + 40*(xloc-1), 10+40*yloc, 50+40*(xloc-1), 10+40*yloc, fill = "LightGray", width = 1)           
        elif (xcor <= 8) or (xcor >= 32) and not ((ycor <= 8) or (ycor >= 32)):  # near a vertical line
            xloc = round((event.x - 10) / 40)   # which column
            yloc = ceil((event.y - 10) / 40)
            if debug:
                print("column: ", xloc, yloc)
            world[yloc*2-1][xloc*2] = not world[yloc*2-1][xloc*2]
            if world[yloc*2-1][xloc*2]:
                awall =aframe.create_line(10 + 40*xloc, 10+40*(yloc-1), 10+40*xloc, 50+40*(yloc-1), fill = "black", width = 3)
            else:
                awall =aframe.create_line(10 + 40*xloc, 10+40*(yloc-1), 10+40*xloc, 50+40*(yloc-1), fill = "white", width = 3)           
                awall =aframe.create_line(10 + 40*xloc, 10+40*(yloc-1), 10+40*xloc, 50+40*(yloc-1), fill = "LightGray", width = 1)           
        else:
            if debug:
                print("null")       

def draw(aframe, world):
    gridwidth = len(world[0]) // 2
    gridheight = len(world) // 2
    for y in range(gridheight):
        for x in range(gridwidth):
            arect=aframe.create_rectangle(10+ 40*x, 10+40*y, 50+40*x, 50+40*y, outline = "LightGray")
    arect=aframe.create_rectangle(10, 10, 50+40*x, 50+40*y, outline = "black", width = 3)

#Menu Actions
def SetWidth(w):
    width = w
    world = makeworld(width, height)
    draw(world)

def SetHeight(h):
    height = h
    world = makeworld(width, height)
    draw(world)


WidthMenu.add_command(label="6", command=SetWidth(6))
WidthMenu.add_command(label="7", command=SetWidth(7))
WidthMenu.add_command(label="8", command=SetWidth(8))
WidthMenu.add_command(label="9", command=SetWidth(9))
WidthMenu.add_command(label="10", command=SetWidth(10))
WidthMenu.add_command(label="11", command=SetWidth(11))
WidthMenu.add_command(label="12", command=SetWidth(12))
WidthMenu.add_command(label="13", command=SetWidth(13))
WidthMenu.add_command(label="14", command=SetWidth(14))
WidthMenu.add_command(label="15", command=SetWidth(15))
WidthMenu.add_command(label="16", command=SetWidth(16))
menubar.add_cascade(label="Width", menu=WidthMenu)
HeightMenu = Menu(menubar)
HeightMenu.add_command(label="6", command=SetHeight(6))
HeightMenu.add_command(label="7", command=SetHeight(7))
HeightMenu.add_command(label="8", command=SetHeight(8))
HeightMenu.add_command(label="9", command=SetHeight(9))
HeightMenu.add_command(label="10", command=SetHeight(10))
HeightMenu.add_command(label="11", command=SetHeight(11))
HeightMenu.add_command(label="12", command=SetHeight(12))
HeightMenu.add_command(label="13", command=SetHeight(13))
HeightMenu.add_command(label="14", command=SetHeight(14))
HeightMenu.add_command(label="15", command=SetHeight(15))
HeightMenu.add_command(label="16", command=SetHeight(16))
menubar.add_cascade(label="Height", menu=HeightMenu)

# set up graphics region
aframe = Canvas(window, width = 800, height = 900)  # create a region for drawing
aframe.pack(side = BOTTOM)
aframe.bind("<Button-1>", lambda event: follow(event, aframe))

world = makeworld( width, height)
draw(aframe, world)

window.mainloop()   #launch the GUI loop

'''
def shift():
    for x in range(50):
        aframe.coords(arect, 10,10,520-10*x,60+x)
        window.update() # update the display 
        window.after(20)
        
def colorswap():
    aframe.itemconfig(arect, outline = ["black", "red", "green", "blue", "cyan", "yellow", "magenta"][randrange(0,6)])
    aframe.itemconfig(arect, fill = ["black", "red", "green", "blue", "cyan", "yellow", "magenta"][randrange(0,6)])

def smile(n):
    aframe.itemconfig(mouthsmile, state = NORMAL)  # show and hide different shapes
    aframe.itemconfig(mouthfrown, state = HIDDEN)
    global smilecounter #need this to be able to change a global variable in a def
    smilecounter += 1   #keep track of how many times the button has been clicked and the procedure called
    print("smile :", n)
    window.update() 

def frown(n):
    aframe.itemconfig(mouthsmile, state = HIDDEN)
    aframe.itemconfig(mouthfrown, state = NORMAL)
    global frowncounter #need this to be able to change a global variable in a def
    frowncounter += 1
    print("frown :", n)
    window.update()

def distance(x1,y1,x2,y2):      # distance formula
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def mousewhere(event):
    global xstart, ystart
    aframe.focus_set() # shift binding to the frame widget.
    boundary = aframe.coords(ball)
##    if (boundary[0] < event.x) and (boundary[2] > event.x) and (boundary[1] < event.y) and (boundary[3] > event.y):
    if distance((boundary[0] + boundary[2])/2, (boundary[1]+ boundary[3])/2, event.x, event.y) < 25:
        xstart = event.x
        ystart = event.y

def followmouse(event):
    global xstart, ystart
    aframe.focus_set() # shift binding to the frame widget.
    if xstart >= 0: # still following mouse
        boundary = aframe.coords(ball)
        aframe.coords(ball, boundary[0] + event.x - xstart, boundary[1] + event.y - ystart, boundary[2] + event.x - xstart, boundary[3] + event.y - ystart)
        xstart = event.x
        ystart = event.y
        
def endfollow(event):  #release object
    global xstart, ystart
    boundary = aframe.coords(ball)
    print(xstart, ystart, event.x, event.y, boundary[0],boundary[1])
    xstart = -1
    ystart = -1
    
    
window = Tk()
window.title('Click Here')
window.minsize(height=600, width=600)
window.config(background="light blue")

aframe = Canvas(window, width = 500, height = 600)  # create a region for drawing
aframe.pack(side = LEFT)
aframe.bind("<Button-1>", mousewhere)
aframe.bind("<B1-Motion>", followmouse)
aframe.bind("<ButtonRelease-1>", endfollow)
ball = aframe.create_oval(100, 100, 150, 150, fill = 'purple')
arect=aframe.create_rectangle(10,10, 500, 60, activeoutline = "red", activedash = (6,2,2,2))

head=aframe.create_oval(200,200, 300, 300,activeoutline = "red", activedash = (2,2))
eye1=aframe.create_oval(230,220,240,230)
eye2=aframe.create_oval(260,220,270,230)
mouthsmile=aframe.create_arc(230,255, 270, 275, start=180, extent=180, outline="green",style=ARC, state = HIDDEN)
mouthfrown=aframe.create_arc(230,260, 270, 280, start=0, extent=180, outline="red", style=ARC, state = HIDDEN)

smilecounter = 0
frowncounter = 0
buttonarea = Frame(window)  # create a region for buttons
buttonarea.pack(side = LEFT)
button1 = Button(buttonarea, text = "Move me!", command = shift)  # bind each button to an action
button1.grid()
button2 = Button(buttonarea, text = "Color me!", command = colorswap)
button2.grid()
button3 = Button(buttonarea, text = "Smile", command = lambda: smile(smilecounter))
button3.grid()  # the lambda above and below are the only way to bind to a def with an argument
button4 = Button(buttonarea, text = "Frown", command = lambda: frown(frowncounter))
button4.grid()

window.mainloop()   #launch the GUI loop
'''

