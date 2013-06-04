# Paul Gribble
# paul [at] gribblelab [dot] org
# June 3, 2013
#
# gradient descent game
# rhythmic back and forth task
# move from one end zone into the other and back again
# experimenter controls weights on two cost parameters:
# movement time and movement curvature at the 50% point

import pygame
import numpy
import math
import sys
import time

numpy.random.seed(int(time.time()))

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
blue     = (   0,   0, 255)

cursorsize = 5    # radius

# Function for computing distance between two (x,y) points
def dist_xyt(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

# Function for displaying text
def printText(txtText, Textfont, Textsize , Textx, Texty, Textcolor):
    # pick a font you have and set its size
    myfont = pygame.font.SysFont(Textfont, Textsize)
    # apply it to text on a label
    label = myfont.render(txtText, 1, Textcolor)
    # put the label object on the screen at point Textx, Texty
    screen.blit(label, (Textx, Texty))

# Setup
pygame.init()
   
# Set the width and height of the screen [width,height]
ssize=[800,400]
screen=pygame.display.set_mode(ssize)

endzone_height = 80 # pixels
endzone1 = endzone_height
endzone2 = ssize[1]-endzone_height

pygame.display.set_caption("yawn")
  
#Loop until done
done=False

# Used to manage how fast the screen updates
clock=pygame.time.Clock()

# Hide the mouse cursor
pygame.mouse.set_visible(0)
 
print "saving to log file %s.asc" % sys.argv[1]
fid = open(sys.argv[1] + ".asc","w")
fid2 = open(sys.argv[1] + ".log","w")

spacebarhit = False

# frames rate
dt = 100
ttotal = 0.0
fps = dt

state = 0
prevstate = 0

# inter-beep interval
ibi = 0

beep1 = pygame.mixer.Sound('23338__altemark__pong.wav')
#beep1 = pygame.mixer.Sound('beep-3.wav')

runtime = 0.0
finishtime = 0.0
xdev = 0.0
cost = 0.0
cost1 = 0.0
cost2 = 0.0

# SET UP THE COST FUNCTION WEIGHTS AND DESIRED VALUES
W1 = 1.0
W2 = 100.0
des_time = 0.750
des_xdev = 30

donetrial = False
ntrials = 0
xstart = 0.0
xdev = 0.0
xprev = 0.0
yprev = 0.0

# -------- Main Program Loop -----------
while done == False:
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        # User pressed down on a key
        if event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_SPACE:
                done = True

    # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
 

    # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT

    # get mouse position
    mx,my = pygame.mouse.get_pos()

    # update state
    if (my < endzone1):
        state = 1         # in endzone 1
    elif (my > endzone2):
        state = 3         # in endzone 2
    elif ((my >= endzone1) and (my <= endzone2)):
        state = 2         # on the field
 
    # endzone to field?
    if ( ((prevstate == 1) or (prevstate == 3)) and (state == 2) ):
        runtime = 0.0
        xstart = mx

    # crossing midpoint?
    if ( (state == 2) and ( (yprev < (ssize[1]/2)) and (my >= ssize[1]/2) ) or ((yprev >= (ssize[1]/2)) and (my < ssize[1]/2)) ):
        xmid = ((xprev + mx) / 2.0)
  
    # field to endzone?
    if ( (prevstate == 2) and ((state == 1) or (state == 3)) ):
        finishtime = runtime
        donetrial = True
        ntrials = ntrials + 1
        xdev = abs(xmid - xstart)
        cost1 = (W1*abs(xdev-des_xdev))
        cost2 = (W2*abs(finishtime-des_time))
        cost = cost1 + cost2
    else:
        donetrial = False

    # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT    
 

    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
      
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(white)
    
    # draw endzone lines
    pygame.draw.lines(screen,red,False,[(0,endzone1),(ssize[0],endzone1)],1)
    pygame.draw.lines(screen,red,False,[(0,endzone2),(ssize[0],endzone2)],1)

    if ((my<endzone1) or (my>endzone2)):
        # draw cursor
        pygame.draw.ellipse(screen,red,[mx,my,cursorsize*2,cursorsize*2],0)

    # draw mouse x,y position
#    printText(repr(mx), "MS Comic Sans", 30, ssize[0]-100, 35, black)
#    printText(repr(my), "MS Comic Sans", 30, ssize[0]-50, 35, black)

    # draw total time and frame rate
#    printText(repr(round(fps*1000)/1000), "MS Comic Sans", 30, 150, 35, black)
#    printText(repr(round(ttotal*1000)/1000), "MS Comic Sans", 30, 50, 35, black)

    # draw runtime and finishtime
#    printText(repr(round(runtime*1000)/1000), "MS Comic Sans", 30, 150, 85, black)
#    printText(repr(round(finishtime*1000)/1000), "MS Comic Sans", 30, 50, 85, black)

    # draw state
#    printText(repr(state), "MS Comic Sans", 30, ssize[0]/2, 35, black)

    # xdev, finishtime, cost
#    printText(repr(round(cost1*1000)/1000), "MS Comic Sans", 30, 50, 10, black)
#    printText(repr(round(cost2*1000)/1000), "MS Comic Sans", 30, 150, 10, black)
    printText(repr(round(cost*1000)/1000), "MS Comic Sans", 30, ssize[0]/2, 10, black)

    # sound
    if (abs(state-prevstate)==1):
        beep1.play()

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
      

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # write data to file
    fid.write("%6.3f %3d %3d %1d\n" % (ttotal,mx,my,state))

    # write log
    if (donetrial == True):
        fid2.write("%3d %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f\n" % (ntrials,W1,W2,des_xdev,des_time,xdev,finishtime,cost))
  
    # Limit to dt frames per second
    clock.tick(dt)
    fps = clock.get_fps()
    inctime = (clock.get_time() / 1000.0)
    ttotal = ttotal + inctime
    
    runtime = runtime + inctime

    prevstate = state
    xprev = mx
    yprev = my

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()

fid.close()
fid2.close()

