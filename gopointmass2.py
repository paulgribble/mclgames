# Paul Gribble
# paul [at] gribblelab [dot] org
# Nov 2, 2012

import pygame
import numpy
import math

numpy.random.seed(10)

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
red      = ( 255,   0,   0)
green    = (   0, 255,   0)
blue     = (   0,   0, 255)

# Function for computing distance to target
def dist_to_target(x,y,tx,ty,params):
    return math.sqrt((x-(tx+params['targetsize']))**2 + (y-(ty+params['targetsize']))**2)

# Function for displaying text
def printText(txtText, Textfont, Textsize , Textx, Texty, Textcolor):
    # pick a font you have and set its size
    myfont = pygame.font.SysFont(Textfont, Textsize)
    # apply it to text on a label
    label = myfont.render(txtText, 1, Textcolor)
    # put the label object on the screen at point Textx, Texty
    screen.blit(label, (Textx, Texty))

# Function to get a new random target
def getnewtarget(state,params):
    cx,cy = params['ssize']/2, params['ssize']/2
    if ((state==1) | (state==6)):
        tx,ty = cx,cy
    else:
        tgtangle = params['tgtlist'][0] * (2*math.pi/params['ntargets'])
        tx = cx + params['ssize']/5 * math.cos(tgtangle)
        ty = cy + params['ssize']/5 * math.sin(tgtangle)
    return tx,ty

# experiment parameters
params = {
    'ntargets'    : 3,    # number of targets per block
    'nblocks'     : 1,    # number of blocks of ntargets
    'homewait'    : 1.0,  # wait time inside home
    'tgtwait'     : 1.0,  # wait time inside target
    'targetsize'  : 30,   # radius (pixels)
    'ballsize'    : 5,    # radius (pixels)
    'ssize'       : 800,  # screen size (pixels)
    'dt'          : 30,   # refresh rate (frames per second)
    'mass'        : 1.0,  # ball mass
    'finc'        : 200,  # force increment per frame
    'fmax'        : 1000, # max force
    'fleak'       : 0.90  # "leakage" of force per frame
}

# Setup
pygame.init()
   
# Set the width and height of the screen [width,height]
screen=pygame.display.set_mode([params['ssize'],params['ssize']])

pygame.display.set_caption("hit the red targets with the black dot")
  
#Loop until the user clicks the close button.
done=False
  
# Used to manage how fast the screen updates
clock=pygame.time.Clock()
 
# Hide the mouse cursor
pygame.mouse.set_visible(0)

# initial position (pixels)
x0,y0 = params['ssize']/2, params['ssize']/2
x,y = x0,y0
# initial vel (pixels/s)
xd,yd = 0.0, 0.0
# initial acc (pixels/s/s)
xdd,ydd = 0.0, 0.0
# initial stim values
kxp,kxn,kyp,kyn = 0.0, 0.0, 0.0, 0.0
# initial muscle forces
xp,xn,yp,yn = 0.0, 0.0, 0.0, 0.0
# initialize score to zero
score = 0

state = 1 # home target visible, waiting to get home
tgtcolour = red

# assemble targets randomized within block
tgtarray = numpy.array([j for j in range(params['ntargets'])], dtype='int')
ntgts = params['nblocks']*params['ntargets']
tgtlist = numpy.array([0 for i in range(ntgts)], dtype='int')
for i in range(params['nblocks']):
    numpy.random.shuffle(tgtarray)
    tgtlist[i*params['ntargets']:(i+1)*params['ntargets']] = tgtarray
# add to params
params['tgtlist'] = list(tgtlist)

# get first target
tx,ty = getnewtarget(state,params)

# initialize timing variables
t_elapsed = 0.0
t_counter = 0.0

# -------- Main Program Loop -----------
while done==False:
    if len(tgtlist) == 0:
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
                kxn = params['finc']
            if event.key == pygame.K_f:
                kxp = params['finc']
            if event.key == pygame.K_j:
                kyp = params['finc']
            if event.key == pygame.K_k:
                kyn = params['finc']
            if event.key == pygame.K_SPACE:
                x = x0
                y = y0
                xd,yd,xdd,ydd = 0,0,0,0
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
                kyp = 0.0
            if event.key == pygame.K_k:
                kyn = 0.0

    # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
 
    # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT

    # convert stim (keypresses) into muscle torque
    xn = min(max((xn + kxn) - (params['finc']*params['fleak']), 0), params['fmax'])
    xp = min(max((xp + kxp) - (params['finc']*params['fleak']), 0), params['fmax'])
    yn = min(max((yn + kyn) - (params['finc']*params['fleak']), 0), params['fmax'])
    yp = min(max((yp + kyp) - (params['finc']*params['fleak']), 0), params['fmax'])
    # forward dynamics
    xdd = (xp-xn) / params['mass']
    ydd = (yp-yn) / params['mass']
    # integrate accelerations into vels
    xd = xd + (xdd/params['dt'])
    yd = yd + (ydd/params['dt'])
    # integrate vels into positions
    x = x + (xd/params['dt'])
    y = y + (yd/params['dt'])

    # boundary detection
    bdec = 0.2
    if x < 0:
        x,xd,xdd = 0,-xd*bdec,-xdd*bdec
    if x > params['ssize']:
        x,xd,xdd = params['ssize'],-xd*bdec,-xdd*bdec
    if y < 0:
        y,yd,ydd = 0,-yd*bdec,-ydd*bdec
    if y > params['ssize']:
        y,yd,ydd = params['ssize'],-yd*bdec,-ydd*bdec

    # state = 1 # home target visible, waiting to get home
    # state = 2 # entered home target, must wait 500 msec
    # state = 3 # waited at home, peripheral target appears
    # state = 4 # peripheral target displayed, waiting to enter peripheral target
    # state = 5 # entered peripheral target, must wait 500 msec
    # state = 6 # waited at peripheral target, home appears
    # state = 7 # all targets complete

    if state==1: # home target displayed, waiting to enter it
        tardist = dist_to_target(x,y,tx,ty,params)
        tgtcolour = red
        if tardist < params['targetsize']: # we entered home target! advance state
            state = 2
            tgtcolour = green # change home colour
            t_counter = t_elapsed
    elif state==2: # check to see if we have waited long enough at home or if we left home early
        if (dist_to_target(x,y,tx,ty,params) < params['targetsize']) & ((t_elapsed-t_counter) > params['homewait']):
            # waited long enough, advance state
            state = 3
            tx,ty = getnewtarget(state,params)
            tgtcolour = red
        elif dist_to_target(x,y,tx,ty,params) > params['targetsize']:
            # oops we left home, restart counter and drop state
            state = 1
            tgtcolour = red
    elif state==3: # peripheral target displayed, waiting to enter it
        if (dist_to_target(x,y,tx,ty,params) < params['targetsize']):
            # we entered the peripheral target, advance state and start counter
            tgtcolour = green
            t_counter = t_elapsed
            state = 4
    elif state==4: # we are in peripheral target, make sure we stay there and wait long enough
        if (dist_to_target(x,y,tx,ty,params) < params['targetsize']) & ((t_elapsed-t_counter) > params['tgtwait']):
            # waited long enough, go to home state
            state = 1
            del params['tgtlist'][0]
            if len(params['tgtlist'])>0:
                tx,ty = getnewtarget(state,params)
            else:
                done = True
                state = 5
        elif dist_to_target(x,y,tx,ty,params) > params['targetsize']:
            # oops we left target early
            state = 3
            tgtcolour = red

#    print state

    # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT    
 
    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
    
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(white)
    
    pygame.draw.ellipse(screen,tgtcolour,[tx,ty,params['targetsize']*2,params['targetsize']*2],0)
    pygame.draw.ellipse(screen,black,[x-params['ballsize'],y-params['ballsize'],params['ballsize']*2,params['ballsize']*2],0)

    printText("Score:", "MS Comic Sans", 30, 10, 10, red)
    printText(repr(score), "MS Comic Sans", 30, 10, 35, red)

    printText("controls:  d f j k", "MS Comic Sans", 30, params['ssize']/2 - 80, 10, red)
    printText("reset:  SPACEBAR", "MS Comic Sans", 30, params['ssize']/2 - 80, 35, red)
    printText("toggle arm:  TAB", "MS Comic Sans", 30, params['ssize']/2 - 80, 60, red)

    printText("Tgts Left:", "MS Comic Sans", 30, params['ssize']-100, 10, red)
    printText(repr(len(params['tgtlist'])), "MS Comic Sans", 30, params['ssize']-100, 35, red)
 
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
      
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
  
    # Limit to dt frames per second
    clock.tick(params['dt'])
    t_elapsed = t_elapsed + (1.0/params['dt'])
      
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
print score

