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
import cPickle
from psychopy.constants import *  # things like STARTED, FINISHED
import wtw # custom wtw helper package
import wtw.drawSample
import wtw.detectResponse
import wtw.handgrip
import wtw.instructions


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
expInfo = {'participant':'', 'order':'0 to 5'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = time.strftime("%d%m%Y") # add a simple timestamp
expInfo['expName'] = expName

### Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# use an ExperimentHandler to handle saving data
# Claudio: try to remove
# thisExp = data.ExperimentHandler(name=expName, version='',
#     extraInfo=expInfo, runtimeInfo=None, originPath=None,
#     savePickle=True, saveWideText=True, dataFileName=filename)

### Check if data folder exists
if os.path.isdir(_thisDir + os.sep + 'data') == False:
    print 'Note: created data directory because none existed'
    os.makedirs('data')

### Setup the Window (size=(2560,1440))
win = visual.Window(
    size=(1280,800), fullscr=False, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True)

# create task stimulus objects
stimObjects = wtw.createStimulusObjects(win,60)
#message = stimObjects['message'] # unpack Claudio, potentially remove

##------------------------ Necessary Handgrip Elements -----------------------
# Just storing what seems necessary. I will need to rearrange everything at some point.
#blockDuration = 15 # in s Claudio: this could be changed to the respective handling time
#fbkDuration = 1 # feedback duration in s
#itiDuration = 1 # in s
#nBlocks = 1
#showInstructions = False
#tokenColorGreen = [-0.3, 0.5, -0.3] # n.b. values range from -1 to 1
#tokenColorPurple = [0.3, -0.5, 0.3]
#tokenColorList = [tokenColorGreen, tokenColorPurple]
#rwdLo = 0 # token reward values Claudio: this will need to change to [5 10 25]
#rwdHi = 10
#rwdUnit = 'pts' # u'\xa2' (the cents character) or 'pts'
#nCbalCells = 1 # number of counterbalance conditions
gripThresholdFraction = 0.20
handgripNeeded = True

# Issue a warning if the handgrip is expected but missing
if LabJack == 0:
    print "WARNING: handgrip device not available."
    warningDlg = gui.Dlg(title="Warning")
    warningDlg.addText('Warning: Handgrip device not available.')
    warningDlg.show()
    if not warningDlg.OK: # if user hit cancel, quit.
        core.quit()

#save a log file for detail verbose info (maybe, just in case)
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

# set up to be able to detect held-down keys
keySH = key.KeyStateHandler()
win.winHandle.push_handlers(keySH)

# initialize variables (meh)
#totalEarned = 0

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
threshold = 0
calibLevel = None
if handgripNeeded:
    calibLevel = wtw.handgrip.calibrate(LabJack, win)
    # calibLevel = {'grip':0.4, 'relax':0} ### FOR TESTING; use this and comment out line above.
    threshold = calibLevel['relax'] + gripThresholdFraction * (calibLevel['grip'] - calibLevel['relax'])
    # log the calibration and resulting threshold
    calibName = filename + '_calibration'
    exp_functions.logwrite(['Median grip','Median relax','Threshold'],calibName)
    exp_functions.logwrite([calibLevel['grip'],calibLevel['relax'],threshold],calibName)
expObjects['thresholdGripStrength'] = threshold
expObjects['calibLevel'] = calibLevel
print 'grip force threshold: ' + str(threshold)
# for data logging
expInfo['gripForceCalibLevels'] = calibLevel
expInfo['gripForceThreshold'] = threshold

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
blockLength = 420 # how long in seconds each timing block will be (60*7)
if blockLength is not 420:
    print 'ERROR: block time is not 7 mins'
    core.quit()
### frameRate (removed the auto-find feature)
frames = 60;

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
rewardOrder = [5,5,10,10,25,25]

##----------------------- Begin experiment ---------------------------------

# initial window, waits for input to begin the experiment
start = visual.TextStim(win, text='Let go of the grip if you want to quit a trial \n\n'+'Press ENTER to begin',height=0.05)
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
        reward.setText(' Next reward = '+str(j)+' points')
        reward.draw()
        win.flip()
        core.wait(2)
        if event.getKeys(keyList=['escape']): #this syntax can be used in the future in case we want to allow quitting during cues
            core.quit()
        trialClock.reset() # sets a timer for the trial
        #####################

        # package parameters for this block
        # Claudio: technically, this is all I need to modify
        blockParams = {}
        #blockParams['blockIdx'] = 1
        #blockParams['drawSample'] = 0 #blockDistribs#[0]
        #blockParams['checkSellResponse'] = wtw.detectResponse.releaseHandGrip #checkSellResponse[blockIdx] #  wtw.detectResponse.releaseHandGrip? function to use for collecting responses
        blockParams['trialLimit'] = handling # float('Inf') # handling?
        #blockParams['blockDuration'] = handling # handling again?
        #blockParams['fbkDuration'] = 1 # feedback duration (1s). Better to remove it.
        #blockParams['itiDuration'] = itiDuration # remove, travel time, feedback and ISI already coded
        #blockParams['rwdLo'] = rwdLo # see how to incorporate. This should be quit, right?
        #blockParams['rwdHi'] = rwdHi # then this should be the possible reward; rwd =  [5 10 25]
        #blockParams['rwdUnit'] = rwdUnit # doesn't matter
        #blockParams['tokenColor'] = tokenColorList[1] # doesn't matter
        #blockParams['totalEarned'] = totalEarned # unneeded

        #physResponse = 0
        # present trials
        physResponse = wtw.showTrials(blockParams, stimObjects, 0, expObjects)
        #thisExp = trialOutput['thisExp']
        #totalEarned = trialOutput['blockParams']['totalEarned']

        ####################
        ## trial response processing
        if physResponse == 1: # if quit # change this to relevant output from handgrip func.
            needsReward = False
            # update logs
            exp_functions.logwrite([handling,j,0,trialClock.getTime(),globalClock.getTime()],filename)
        else:
            # Give reward once block is completed
            # update logs
            exp_functions.logwrite([handling,j,1,trialClock.getTime(),globalClock.getTime()],filename)
            # update the reward earned so far
            rewardAmount += j
            reward.setText('Trial completed \n' + 'You earned '+str(j)+' points')
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
start.setText('Great work! You earned ' + str(rewardAmount) + ' points')
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
