#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division
from psychopy import gui, visual, core, event
import numpy as np  # whole numpy lib is available, prepend 'np.'
import os  # handy system and path functions
import sys  # to get file system encoding
import time
import exp_functions


##------------------------ Basic experiment settings -------------------------
#### Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

#### Store info about the experiment session
expName = 'wait'  # from the Builder filename that created this script
expInfo = {'participant':'', 'order':'0 to 5'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = time.strftime("%d%m%Y") # add a simple timestamp
expInfo['expName'] = expName

### Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
filename2 = u'data/attention_%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

### Check if data folder exists
if os.path.isdir(_thisDir + os.sep + 'data') == False:
    print 'Note: created data directory because none existed'
    os.makedirs('data')

### Setup the Window
win = visual.Window(
    size=(2560,1440), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True)

##-------------------- Setting up stimuli, etc. ----------------------------
### Reward stimulus. Text modified per trial
reward = visual.TextStim(win,height=0.08,text='$0.25')
### Traveling stimuli
traveling = visual.TextStim(win, text='Traveling',height=0.08,pos=(0.0,0.0)) # Just the text
travel1 = visual.Rect(win=win,height=0.1,width=500,lineWidth=2,lineColor='white',pos=(0.0,-0.55)) # Bar borders (width=((set_timing*60)/1000))
travel2 = visual.Rect(win=win,height=0.1,width=0.1, fillColor='green',pos=(0.0,-0.55)) # Green progress bar
### ISI stimulus
isi = visual.TextStim(win, text='+')
### timing cue stimulus
timing = visual.TextStim(win=win,text='Travel time = x seconds',height=0.08,pos=(0.0,0.0))
### Cummulative reward amount
rewardAmount = 0
### task lengths
blockLength = 420 # how long in seconds each timing block will be
if blockLength is not 420:
    print 'ERROR: block time is not 7 mins'
    core.quit()
### frameRate (removed the auto-find feature)
frames = 60;


### set clocks
globalClock = core.Clock() # experiment timer
blockClock = core.Clock() # block timer
trialClock = core.Clock() # trial timer

### Order of the conditions and the mental tasks
# based on a latin square (half of the matrix), only one row will be used
# once half of the row is reached, there's a break and then the same order is presented
blockOrder = [[(2,14),(6,10),(14,2),(2,14),(6,10),(14,2)],
              [(6,10),(14,2),(2,14),(6,10),(14,2),(2,14)],
              [(14,2),(2,14),(6,10),(14,2),(2,14),(6,10)],
              [(2,14),(14,2),(6,10),(2,14),(14,2),(6,10)],
              [(6,10),(2,14),(14,2),(6,10),(2,14),(14,2)],
              [(14,2),(6,10),(2,14),(14,2),(6,10),(2,14)]]
### selected block order from initial dialogue input
blockOrder = blockOrder[int(expInfo['order'])]
rewardOrder = [4,4,8,8,20,20]

##----------------------- Begin experiment ---------------------------------

# initial window, waits for input to begin the experiment
start = visual.TextStim(win, text='Press space if you want to quit a trial \n'+'Press ENTER to begin',height=0.05)
start.draw()
win.flip()
event.waitKeys(keyList=['return'])

globalClock.reset()  # to track the time since experiment started

##----------------------- Overall condition loop ---------------------------

for k in range(len(blockOrder)):
    if k == (len(blockOrder)/2): # get a break halfway through
        exp_functions.logwrite([0,0,0,0,globalClock.getTime()],filename)
        start.setText('You are halfway there. Take a break if you want! \n'+'Press ENTER to continue.')
        start.draw()
        win.flip()
        event.waitKeys(keyList=['return'])
    travel = blockOrder[k][0]
    handling = blockOrder[k][1]
    # timing cue
    isi.draw()
    win.flip()
    core.wait(1)
    # this part could possibly be recoded with % placeholders
    timing.setText('Handling time ='+' '+str(handling)+' '+'seconds \n'+'Travel time ='+' '+str(travel)+' '+'seconds')
    travel1.setWidth((travel*frames)/1000)
    travel1.setFillColor('green')
    timing.draw()
    travel1.draw()
    win.flip()
    core.wait(4)
    travel1.setFillColor(None) # otherwise the bar will just be invariant below
    # track how long each timing block is (e.g. 2.5 mins each for a 10 min session)
    blockClock.reset()
    event.clearEvents()
    counter = 0 # to help distribute rewards more evenly
    # Begin trials
    while blockClock.getTime() < blockLength:
        if counter == 0:
            np.random.shuffle(rewardOrder)
        j = rewardOrder[counter]
        needsReward = True # changes to False if the participant quits the block
        reward.setText(' Next reward = '+str(j)+' cents')
        reward.draw()
        win.flip()
        core.wait(2)
        if event.getKeys(keyList=['escape']): #this syntax can be used in the future in case we want to allow quitting during cues
            core.quit()
        trialClock.reset() # sets a timer for the trial
        # Calls the wait block function, handling = length of block
        waitResponse = exp_functions.waitCondition(win,handling)

        ## Wait block response processing
        if waitResponse == 1: # if quit
            needsReward = False
            # update logs
            exp_functions.logwrite([handling,j,0,trialClock.getTime(),globalClock.getTime()],filename)
        else:
            # Give reward once block is completed
            # update logs
            exp_functions.logwrite([handling,j,1,trialClock.getTime(),globalClock.getTime()],filename)
            # update the reward earned so far
            rewardAmount += j
            reward.setText('Trial completed \n' + 'You earned '+str(j)+' cents')
            reward.draw()
            win.flip()
            core.wait(2)

        # traveling
        travel1.setWidth((travel*frames)/1000)
        travel1.setAutoDraw(True)
        traveling.setAutoDraw(True)
        win.flip()
        for i in range(travel*frames):
            if event.getKeys(keyList=['escape']): #this syntax can be used in the future in case we want to allow quitting during cues
                core.quit()
            travel2.setWidth(i/1000)
            travel2.draw()
            win.flip()
        traveling.setAutoDraw(False)
        travel1.setAutoDraw(False)

        if counter == 5:
            counter = 0
        else:
            counter += 1

        if (blockLength - blockClock.getTime()) < 8: # this sudden break is to control for most blocks being larger than their supposed length
            break

    # Attention trial
    blockClock.reset()
    event.clearEvents()
    isi.setText('Press space to go to the next block')
    isi.setAutoDraw(True)
    win.flip()
    event.waitKeys(maxWait = 30, keyList = ['space'])
    exp_functions.logwrite([k + 1,blockClock.getTime(),globalClock.getTime()],filename2)
    isi.setAutoDraw(False)
    isi.setText('+')

## Final screen showing final reward amount
start.setText('Great work! You earned ' + '$' + str((rewardAmount+1200)/100.0))
start.draw()
win.flip()
event.waitKeys(keyList=['return'])

# close Window
win.close()

# close PsychoPy
core.quit()
