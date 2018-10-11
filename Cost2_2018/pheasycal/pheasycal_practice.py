#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division
from psychopy import gui, visual, core, event, data, logging #, sound
import numpy as np  # whole numpy lib is available, prepend 'np.'
import os  # handy system and path functions
import sys  # to get file system encoding
import csv
import time
import exp_functions
# handgrip
from pyglet.window import key
from psychopy.constants import *  # things like STARTED, FINISHED
import wtw # custom wtw helper package
import wtw.drawSample
import wtw.detectResponse
import wtw.handgrip

# Evaluate whether LabJack DAQ and the u3 module are both available
# if so, the LabJack variable holds the DAQ object, otherwise it's set to zero.
LabJack = 0
try:
    import u3 # LabJack package
    LabJack = wtw.handgrip.openLabJack(u3)
except:
    pass

##------------------------ Basic experiment settings -------------------------
#### Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

#### Store info about the experiment session
expName = 'physSona'  # from the Builder filename that created this script
expInfo = {'participant':'', 'order':'0'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = time.strftime("%d%m%Y") # add a simple timestamp
expInfo['expName'] = expName

### Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

### Check if data folder exists
if os.path.isdir(_thisDir + os.sep + 'data') == False:
    print 'Note: created data directory because none existed'
    os.makedirs('data')

### Setup the Window (size=(2560,1440))
win = visual.Window(
    size=(1280,800), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True)

# create task stimulus objects
stimObjects = wtw.createStimulusObjects(win,60)

##------------------------ Necessary Handgrip Elements -----------------------

gripThresholdFraction = 0.05
handgripNeeded = True

# Issue a warning if the handgrip is expected but missing
if LabJack == 0:
    print "WARNING: handgrip device not available."
    warningDlg = gui.Dlg(title="Warning")
    warningDlg.addText('Warning: Handgrip device not available.')
    warningDlg.show()
    if not warningDlg.OK: # if user hit cancel, quit.
        core.quit()

# set up to be able to detect held-down keys
keySH = key.KeyStateHandler()
win.winHandle.push_handlers(keySH)

### set clocks
globalClock = core.Clock() # experiment timer
blockClock = core.Clock() # block timer
trialClock = core.Clock() # trial timer

# package some general objects to pass to the trial display function
expObjects = {}
expObjects['win'] = win
expObjects['blockClock'] = blockClock
expObjects['keySH'] = keySH
expObjects['LabJack'] = LabJack
expObjects['handgripNeeded'] = handgripNeeded
expObjects['filename'] = filename

# calibrate participant's baseline hand grip if needed. Claudio: this will have to go at the beginning.
# Claudio: no calibration here, to avoid doing it twice and giving participants the option to modulate their threshold
threshold = 0
calibLevel = None
if handgripNeeded:
    #calibLevel = wtw.handgrip.calibrate(LabJack, win)
    calibLevel = {'grip':0.4, 'relax':0.2} ### FOR TESTING; use this and comment out line above.
    threshold = calibLevel['relax'] + gripThresholdFraction * (calibLevel['grip'] - calibLevel['relax'])
    # log the calibration and resulting threshold
    calibName = filename + '_calibration'
expObjects['thresholdGripStrength'] = threshold
expObjects['calibLevel'] = calibLevel
print 'grip force threshold: ' + str(threshold)

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
blockLength = 120 # how long in seconds each timing block will be (60*7)

### frameRate (removed the auto-find feature)
frames = 60;

### Order of the conditions and the mental tasks
# based on a latin square (half of the matrix), only one row will be used
# once half of the row is reached, there's a break and then the same order is presented
blockOrder = [[4,8]]
### selected block order from initial dialogue input
rewardOrder = [4,4,8,8,20,20]

##----------------------- Begin experiment ---------------------------------

# initial window, waits for input to begin the experiment
start = visual.TextStim(win, text='Let go of the grip if you want to quit a trial \n\n'+'Press ENTER to begin',height=0.05)
start.draw()
win.flip()
event.waitKeys(keyList=['return'])

globalClock.reset()  # to track the time since experiment started

##----------------------- Overall condition loop ---------------------------

for k in range(len(blockOrder)):
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
        # package parameters for this block
        blockParams = {}
        blockParams['trialLimit'] = handling # float('Inf') # handling?

        # present trials
        physResponse = wtw.showTrials(blockParams, stimObjects, 0, expObjects)

        ## trial response processing
        if physResponse == 1: # if quit # change this to relevant output from handgrip func.
            needsReward = False
            # update logs
            #exp_functions.logwrite([handling,j,0,trialClock.getTime(),globalClock.getTime()],filename)
        else:
            # Give reward once block is completed
            # update logs
            #exp_functions.logwrite([handling,j,1,trialClock.getTime(),globalClock.getTime()],filename)
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

## Final screen showing final reward amount
start.setText('Great work! You earned ' + '$' + str((rewardAmount+1200)/100.0))
start.draw()
win.flip()
event.waitKeys(keyList=['return'])

# close Window
win.close()

# close Lab Jack
if LabJack != 0:
    LabJack.close() # close LabJack connection

# close PsychoPy
core.quit()
