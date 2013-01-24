# Paul Gribble
# paul [at] gribblelab [dot] org
# Nov 2, 2012

import pygame
import numpy
import math

numpy.random.seed(10)

showarm = True

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)

targetsize = 30 # radius
ballsize = 5 # radius

# Function for computing distance to target
def dist_to_target(x,y,tx,ty):
    return math.sqrt((x-(tx+targetsize))**2 + (y-(ty+targetsize))**2)

# Function for displaying text
def printText(txtText, Textfont, Textsize , Textx, Texty, Textcolor):
    # pick a font you have and set its size
    myfont = pygame.font.SysFont(Textfont, Textsize)
    # apply it to text on a label
    label = myfont.render(txtText, 1, Textcolor)
    # put the label object on the screen at point Textx, Texty
    screen.blit(label, (Textx, Texty))

# Function to get a new random target
def getnewtarget(ssize):
    # random
    xmin,xmax = 50,ssize[0]-50
    ymin,ymax = 100,ssize[0]-50
    tx = (numpy.random.random() * (xmax-xmin)) + xmin
    ty = (numpy.random.random() * (ymax-ymin)) + ymin
    return tx,ty

# Setup
pygame.init()
   
# Set the width and height of the screen [width,height]
ssize=[800,800]
screen=pygame.display.set_mode(ssize)

pygame.display.set_caption("hit the red targets with the black dot")
  
#Loop until the user clicks the close button.
done=False
  
# Used to manage how fast the screen updates
clock=pygame.time.Clock()
 
# Hide the mouse cursor
pygame.mouse.set_visible(0)
 
# time increment (frames per second)
dt = 30.0
dti = 1.0/dt

m = 1.0 # kg
# keypress force
finc = 200.0   # force increment per frame
fmax = 1000.0
fleak = 0.90 # "leakage" of force per frame
maxvel = 30.0
maxacc = 300.0

# initial position (pixels)
x0 = ssize[0]/2
y0 = ssize[1]/2
x,y = x0,y0

# initial vel (pixels/s)
xd = 0.0
yd = 0.0

# initial acc (pixels/s/s)
xdd=0.0
ydd=0.0

# initial stim values
kxp = 0.0
kxn = 0.0
kyp = 0.0
kyn = 0.0

# initial muscle forces
xp = 0.0
xn = 0.0
yp = 0.0
yn = 0.0

ttotal = 0.0
score = 0
timelimit = 60.0

# target
tx,ty = getnewtarget(ssize)

# -------- Main Program Loop -----------
while done==False:
    if ttotal >= timelimit:
        done=True
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
            # User pressed down on a key
         
        if event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_d:
                kxn = finc
            if event.key == pygame.K_f:
                kxp = finc
            if event.key == pygame.K_j:
                kyn = finc
            if event.key == pygame.K_k:
                kyp = finc
            if event.key == pygame.K_SPACE:
                x = x0
                y = y0
                xd = 0
                yd = 0
                xdd = 0
                ydd = 0
                xn,xp,yn,yp = 0,0,0,0
                score = score-1
                if (score<0):
                    score = 0
            if event.key == pygame.K_TAB:
                showarm = not showarm

        # User let up on a key
        if event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_d:
                kxn = 0.0
            if event.key == pygame.K_f:
                kxp = 0.0
            if event.key == pygame.K_j:
                kyn = 0.0
            if event.key == pygame.K_k:
                kyp = 0.0

    # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
 
    # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT

    # convert stim (keypresses) into muscle torque
    xn = min(max((xn + kxn) - (finc*fleak), 0), fmax)
    xp = min(max((xp + kxp) - (finc*fleak), 0), fmax)
    yn = min(max((yn + kyn) - (finc*fleak), 0), fmax)
    yp = min(max((yp + kyp) - (finc*fleak), 0), fmax)

    # forward dynamics

    xdd = (xp-xn) / m
    ydd = (yp-yn) / m

    # integrate accelerations into vels
    xd = xd + (xdd*dti)
    yd = yd + (ydd*dti)

    # integrate vels into positions
    x = x + (xd*dti)
    y = y + (yd*dti)

    # boundary detection
    bdec = 0.2
    if x < 0:
        x,xd,xdd = 0,-xd*bdec,-xdd*bdec
    if x > ssize[0]:
        x,xd,xdd = ssize[0],-xd*bdec,-xdd*bdec
    if y < 0:
        y,yd,ydd = 0,-yd*bdec,-ydd*bdec
    if y > ssize[1]:
        y,yd,ydd = ssize[1],-yd*bdec,-ydd*bdec

    # target hit detection
    tardist = dist_to_target(x,y,tx,ty)
    if  tardist < targetsize:
        score = score + 1
        tx,ty = getnewtarget(ssize)
 
    # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT    
 
    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
    
#    print x,y
#    print xn,xp,yn,yp

    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(white)
    
    pygame.draw.ellipse(screen,red,[tx,ty,targetsize*2,targetsize*2],0)
    pygame.draw.ellipse(screen,black,[x-ballsize,y-ballsize,ballsize*2,ballsize*2],0)

    printText("Score:", "MS Comic Sans", 30, 10, 10, red)
    printText(repr(score), "MS Comic Sans", 30, 10, 35, red)

    printText("controls:  d f j k", "MS Comic Sans", 30, ssize[0]/2 - 80, 10, red)
    printText("reset:  SPACEBAR", "MS Comic Sans", 30, ssize[0]/2 - 80, 35, red)
    printText("toggle arm:  TAB", "MS Comic Sans", 30, ssize[0]/2 - 80, 60, red)

    printText("Time:", "MS Comic Sans", 30, ssize[0]-100, 10, red)
    printText(repr(round(timelimit-ttotal,1)), "MS Comic Sans", 30, ssize[0]-100, 35, red)
 
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
      
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
  
    # Limit to dt frames per second
    clock.tick(dt)
    ttotal = ttotal + dti
      
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
print score

