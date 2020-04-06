# Paul Gribble
# Oct 18, 2012
  
import pygame
import numpy
import math
  
# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
 
# Function to draw our stick figure
def draw_ball(screen,x,y):
    pygame.draw.ellipse(screen,black,[x,y,10,10],0)
     
# Setup
pygame.init()
   
# Set the width and height of the screen [width,height]
ssize=[800,800]
screen=pygame.display.set_mode(ssize)
  
pygame.display.set_caption("My Game")
  
#Loop until the user clicks the close button.
done=False
  
# Used to manage how fast the screen updates
clock=pygame.time.Clock()
 
# Hide the mouse cursor
pygame.mouse.set_visible(0)
 
# initial position
x0=200.0
y0=400.0
x=x0
y=y0

# initial vel (pixels per frame)
xd=0.0
yd=0.0

# initial acc (pixels per frame per frame)
xdd=0.0
ydd=0.0

# rockets thrust
r1 = 0.0
r2 = 0.0
r3 = 0.0
r4 = 0.0

# time increment (frames per second)
dt = 30.0
dti = 1.0/dt

# keypress acceleration per frame (pixels/frame/frame)
ak = 500.0

M = numpy.eye(4)
#M = numpy.random.rand(4,4) - 0.5

ttotal = 0.0

# -------- Main Program Loop -----------
while done==False:
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
            # User pressed down on a key
         
        if event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_d:
                r1 = ak
            if event.key == pygame.K_f:
                r2 = ak
            if event.key == pygame.K_j:
                r3 = ak
            if event.key == pygame.K_k:
                r4 = ak
            if event.key == pygame.K_SPACE:
                x = x0
                y = y0
                xd = 0
                yd = 0
                xdd = 0
                ydd = 0

        # User let up on a key
        if event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_d:
                r1 = 0.0
            if event.key == pygame.K_f:
                r2 = 0.0
            if event.key == pygame.K_j:
                r3 = 0.0
            if event.key == pygame.K_k:
                r4 = 0.0

    # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
 
    # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
 
    # Move the object according to the speed vector.

    rockets = numpy.matrix([r1,r2,r3,r4])
    acc = rockets * M
    # left,right,up,down
    xdd = acc[0,1] - acc[0,0]
    ydd = acc[0,3] - acc[0,2]
    print(xdd,ydd)
#    xgrav = 0.0
#    ygrav = ak/2*dti
    xgrav = (ak/2*dti) * math.cos(2*math.pi*ttotal/10.0)
    ygrav = (ak/2*dti) * math.cos(2*math.pi*ttotal/10.0)
    xd = xd + (xdd*dti) + xgrav
    yd = yd + (ydd*dti) + ygrav
    if (x + (xd*dti) > ssize[0]) | (x + xd*dti < 0):
        xd = xd * -1
    if (y + (yd*dti) > ssize[1]) | (y + yd*dti < 0):
        yd = yd * -1
    x = x + (xd*dti)
    y = y + (yd*dti)
 
    # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT    
 
    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
      
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(white)
     
    pygame.draw.ellipse(screen,red,[600,100,50,50],0)
    draw_ball(screen,x,y) 
 
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
      
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
  
    # Limit to dt frames per second
    clock.tick(dt)
    ttotal = ttotal + dt
      
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
