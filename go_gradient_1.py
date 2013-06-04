# Paul Gribble
# paul [at] gribblelab [dot] org
# June 3, 2013
#
# gradient descent game
# rhythmic back and forth task
# move from one end zone into the other and back again
# experimenter controls weights on two cost parameters:
# movement time and movement curvature at the 50% point

# NOTES
# on a per-subject basis, do a calibration block where xdev_des = 0.0 and speed_des = 0.500
# measure variance in each control df
# then scale feedback gains accordingly
# this way relationship between feedback and control df is equalized across df and across subjects


import pygame
import numpy
import math
import sys
import time
import os

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

# turn of mouse acceleration
os.system("xinput --set-prop 8 267 1.0")
# slow down speed gain to make 1cm on table == 1cm on screen
os.system("xinput --set-prop 8 265 4.25")
# note "8" is the device id and may be different on other machines

# Setup
pygame.init()
   
# Set the width and height of the screen [width,height]
ssize=[800,700]
screen=pygame.display.set_mode(ssize)

endzone_height = 100 # pixels
endzone1 = endzone_height
endzone2 = ssize[1]-endzone_height
eoffset = 10

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

# frame rate
dt = 100
ttotal = 0.0
fps = dt

state = 0
prevstate = 0

# inter-beep interval
ibi = 0

#beep1 = pygame.mixer.Sound('23338__altemark__pong.wav')
beep1 = pygame.mixer.Sound('newpong.wav')
#beep1 = pygame.mixer.Sound('beep-3.wav')

runtime = 0.0
finishtime = 0.0
xdev = 0.0
cost = 0.0
cost1 = 0.0
cost2 = 0.0
coins = 1000

# SET UP THE COST FUNCTION WEIGHTS AND DESIRED VALUES
W1 = 0.100        # on xdev
#W1 = 0.000       # on xdev
#des_xdev = 80      # pixels
W2 = 100.00        # on timing
#W2 = 0.0
#des_time = 0.500  # seconds

# input arguments
des_xdev = int(sys.argv[2])
des_time = float(sys.argv[3])
des_trials = int(sys.argv[4])

donetrial = False
ntrials = 0
#des_trials = 50
xstart = 0.0
xdev = 0.0
xprev = 0.0
yprev = 0.0

showtraj = False
showtrajcount = 0
showtrajframes = int(dt * 0.250) # seconds

movdir = 0 # 0=forward, 1=backward

print "%s %d %6.3f %d" % (sys.argv[1],des_xdev,des_time,des_trials)

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
        beep1.play()
        runtime = 0.0
        xstart = mx
        # which direction?
        if ( (prevstate == 1) and (state == 2) ):
            movdir = 0
        elif ( (prevstate == 3) and (state == 2) ):
            movdir = 1

    # field to endzone?
    if ( (prevstate == 2) and ((state == 1) or (state == 3)) ):
        beep1.play()
        finishtime = runtime
        donetrial = True
        ntrials = ntrials + 1
        xend = mx # if endzone is the key
        if (movdir == 0):
            xdev = (xend - xstart)
        elif (movdir == 1):
            xdev = (xstart - xend)
        cost1 = (W1*abs(xdev-des_xdev))
        cost2 = (W2*abs(finishtime-des_time))
        cost = cost1 + cost2
        coins = coins - int(cost)
        # flag to show trajectory slant
        showtraj = True
        showtrajcount = 0
        if (ntrials == des_trials):
            done = True
    else:
        donetrial = False

    if (showtraj == True):
        showtrajcount = showtrajcount + 1

    if ( (showtrajcount <= showtrajframes) and (showtraj == True) ):
        showtraj = True
    else:
        showtraj = False

    # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT    
 

    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
      
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(white)
    
    # draw endzone lines
    pygame.draw.lines(screen,red,False,[(0,endzone1-eoffset),(ssize[0],endzone1-eoffset)],1)
    pygame.draw.lines(screen,red,False,[(0,endzone2+eoffset),(ssize[0],endzone2+eoffset)],1)

#    if ((my<endzone1) or (my>endzone2)):
#        # draw cursor
#        pygame.draw.ellipse(screen,red,[mx,my,cursorsize*2,cursorsize*2],0)
    pygame.draw.ellipse(screen,red,[mx,my,cursorsize*2,cursorsize*2],0)

    # show trajectory slant?
    if (showtraj == True):
        if (movdir == 0):
            yez1 = endzone1 - eoffset
            yez2 = endzone2 + eoffset
        elif (movdir == 1):
            yez1 = endzone2 + eoffset
            yez2 = endzone1 - eoffset
        pygame.draw.lines(screen,blue,False,[(xstart,yez1),(xend,yez2)],1)

    # show some stuff to the user
    printText(repr(int(des_trials-ntrials)),  "MS Comic Sans", 30, ssize[0]/2 - 50, 10, black)
    printText(repr(int(cost)),  "MS Comic Sans", 30, ssize[0]/2, 10, black)
    printText(repr(int(coins)), "MS Comic Sans", 30, ssize[0]/2 + 50, 10, black)

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT


    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # write data to file
    fid.write("%6.3f %3d %3d %1d\n" % (ttotal,mx,my,state))

    # write to logfile
    if (donetrial == True):
        fid2.write("%3d %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %d %d\n" % (ntrials,W1,W2,des_xdev,des_time,xdev,finishtime,cost,int(cost),coins))
        print "%3d %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %d %d" % (ntrials,W1,W2,des_xdev,des_time,xdev,finishtime,cost,int(cost),coins)
  
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

screen.fill(white)
printText(repr(int(coins)), "MS Comic Sans", 200, 250, 300, black)
pygame.display.flip()

pygame.time.wait(2000)

pygame.quit ()

# turn of mouse acceleration
os.system("xinput --set-prop 8 267 10.0")
# slow down speed gain to make 1cm on table == 1cm on screen
os.system("xinput --set-prop 8 265 1.0")
# note "8" is the device id and may be different on other machines

fid.close()
fid2.close()

