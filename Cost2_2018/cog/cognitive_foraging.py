#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division
from psychopy import gui, visual, core, event
import numpy as np  # whole numpy lib is available, prepend 'np.'
import os  # handy system and path functions
import sys  # to get file system encoding
import csv
import time
import exp_functions


##------------------------ Basic experiment settings -------------------------
### Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

### Store info about the experiment session
expName = 'cogTask'  # from the Builder filename that created this script
expInfo = {'participant':'', 'order':'0 to 5'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = time.strftime("%d%m%Y")#data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

### log file name
## log order: 'timing','Expected Reward','Decision (0=quit;1=complete; 2=failed)','RT','Trial Time','Total Time','Trial result','Task presentec','Parameters used'
#filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date']) # old
filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
filename2 = u'data/attention_%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

### Check if data folder exists
if os.path.isdir(_thisDir + os.sep + 'data') == False:
    print 'NOTE: Created data directory because none existed'
    os.makedirs('data')

### Setup the Window
win = visual.Window(
    size=(2560, 1440), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True)

##-------------------- Setting up stimuli, etc. ----------------------------
### Reward stimuli. Text modified per trial
reward = visual.TextStim(win,height=0.08,text='$0.25')
### Traveling stimuli
traveling = visual.TextStim(win, text='Traveling',height=0.08,pos=(0.0,0.0)) # Just the text
travel1 = visual.Rect(win=win,height=0.1,width=100,lineWidth=2,lineColor='white',pos=(0.0,-0.55)) # Bar borders (width=((k*60)/1000))
travel2 = visual.Rect(win=win,height=0.1,width=100, fillColor='green',pos=(0.0,-0.55)) # Green progress bar
### ISI stimulus
isi = visual.TextStim(win, text='+')
### timing cue stimulus
timing = visual.TextStim(win=win,text='Travel time = x seconds',height=0.08,pos=(0.0,0.0))
### Cummulative reward amount
rewardAmount = 0
### timing parameters
taskTime = 1 # for each mental task
isiTime = 2 - taskTime # tentative, as dealing with 2s makes parameterizing easier
blockLength = 420 # how long in seconds each timing block will be. This controls the total experiment time
if blockLength is not 420:
    print 'ERROR: block time is not 7 mins'
    core.quit()
### frameRate (removed the auto-find feature)
frames = 60;

### Importing task parameters
## Stroop
stroopColor = []
stroopWord = []
leftColor = []
rightColor = []
corrStroop = []
## Flanker
flankType = []
corrFlank = []
## Dot motion
coherDots = []
direcDots = []
corrDots = []

### Open the conditions file to begin import
# The order of the columns in the .csv file should be:
# stroopWord,stroopColor,leftColor,rightColor,corrStroop,flankType,corrFlank,coherDots,direcDots,corrDots
condfile = open('conditions.csv','rU') # traditionally, rb should work. However, Mac inputs \r as line delimiter, so rU changes that to \n instead. See 'open' for info
reader = csv.reader(condfile,delimiter=',')
for row in reader:
    stroopWord.append(row[0])
    stroopColor.append(row[1])
    leftColor.append(row[2])
    rightColor.append(row[3])
    corrStroop.append(row[4])
    flankType.append(row[5])
    corrFlank.append(row[6])
    coherDots.append(float(row[7]))
    direcDots.append(float(row[8]))
    corrDots.append(row[9])
condfile.close()

### set clocks
globalClock = core.Clock() # experiment timer
blockClock = core.Clock() # block timer
trialClock = core.Clock() # trial timer

### Order of the conditions and the mental tasks
# each combo is (travel,handling)
# based on a latin square (half of the matrix), only one row will be used
blockOrder = [[(2,14),(6,10),(14,2),(2,14),(6,10),(14,2)],
              [(6,10),(14,2),(2,14),(6,10),(14,2),(2,14)],
              [(14,2),(2,14),(6,10),(14,2),(2,14),(6,10)],
              [(2,14),(14,2),(6,10),(2,14),(14,2),(6,10)],
              [(6,10),(2,14),(14,2),(6,10),(2,14),(14,2)],
              [(14,2),(6,10),(2,14),(14,2),(6,10),(2,14)]]
### selected block order from initial dialogue input
blockOrder = blockOrder[int(expInfo['order'])]
rewardOrder = [4,4,8,8,20,20]
### to set an upper limit for the isi (prevents lag accrual)
goUntil = [2,4,6,8,10,12,14]

##----------------------- Begin experiment ---------------------------------

### initial window, waits for input to begin the experiment
start = visual.TextStim(win, text='Remember: respond with the left or right keys \n' + 'Press space to quit each condition \n'+'Press ENTER to begin',height=0.05)
start.draw()
win.flip()
event.waitKeys(keyList=['return'])

globalClock.reset()  # reset to track the time since 'Enter' was pressed

##----------------------- Overall condition loop ---------------------------

for k in range(len(blockOrder)):
    if k == (len(blockOrder)/2): # get a break halfway through
        exp_functions.logwrite([0,0,0,99,0,globalClock.getTime(),'Break',0,0],filename) # rt = 99 so it complies with logread.m
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
    counter = 0 # to help distribute rewards more evenly
    # Begin trials
    while blockClock.getTime() < blockLength:
        # look into seeding
        if counter == 0:
            np.random.shuffle(rewardOrder)
        j = rewardOrder[counter]
        needsReward = True # changes to False if the participant quits the block
        miss = 0 # keeps track of incorrect answers or misses
        reward.setText('Next reward = '+str(j)+' cents')
        reward.draw()
        win.flip()
        core.wait(2)
        if event.getKeys(keyList=['escape']): #this syntax can be used in the future in case we want to allow quitting during cues
            core.quit()
        # temporary solution to the trial length. I need to recalculate the optimal behavior at 16 seconds so dividing handling by 2 remains an integer
        mentalOrder = np.random.randint(0,high=3,size=int(round(handling/(taskTime+isiTime)))) # array of random integers (1 to 3) to select each task
        trialClock.reset() # resets a timer for the trial
        event.clearEvents()
        # trial of tasks begins here
        for count, i in enumerate(mentalOrder):
            taskResponse = None
            param = np.random.randint(0,8) # chooses an integer to be used as the parameter index
            if i == 0:
                # Calls the stroop task function with the following order of inputs:
                # (word color, word, color on the left, color on the right, correct answer left-right, win (window),time of task)
                taskResponse = exp_functions.stroopCondition(stroopColor[param],stroopWord[param],leftColor[param],rightColor[param],corrStroop[param],win,taskTime)

            elif i == 1:
                # Calls the flanker task function with the following order of inputs:
                # (flanker type, correct answer left-right, win (window),time of task)
                taskResponse = exp_functions.flankerCondition(flankType[param],corrFlank[param],win,taskTime)

            elif i == 2:
                # Calls the dot task function with the following order of inputs:
                # (coherence, direction of dots, correct answer left (180)-right (360), win (window),time of task)
                taskResponse = exp_functions.dotsCondition(coherDots[param],direcDots[param],corrDots[param],win,taskTime)

            ## ISI
            if taskResponse[0] is not 1:
                timeLeft = goUntil[count] - trialClock.getTime()
                isi.setAutoDraw(True)
                win.flip()
                for l in range(int(timeLeft*frames)):
                    win.flip()
                    if 'space' in event.getKeys(keyList='space'):
                        taskResponse = (1, trialClock.getTime())
                        break
                isi.setAutoDraw(False)

            ## taskResponse processing and logging
            # if space was pressed, break the loop and log it as a 1 (quit), otherwise log correct/incorrect responses onto resp_log as coded above
            if taskResponse[0] == 2: # if correct
                # update log
                exp_functions.logwrite([handling,j,1,taskResponse[1],trialClock.getTime(),globalClock.getTime(),0,i,param],filename)
            elif taskResponse[0] == 1: # if quit
                needsReward = False
                # update log for the task
                exp_functions.logwrite([handling,j,0,taskResponse[1],trialClock.getTime(),globalClock.getTime(),0,i,param],filename)
                # update log to note the end of the trial
                exp_functions.logwrite([handling,j,0,0,trialClock.getTime(),globalClock.getTime(),'Quit',0,0],filename)
                break
            elif taskResponse[0] == 3: # if missed or wrong
                miss += 1
                # update log
                exp_functions.logwrite([handling,j,2,taskResponse[1],trialClock.getTime(),globalClock.getTime(),0,i,param],filename)

            if (miss == 1 and handling == 2) or (miss > 1): # quit if too many errors or misses
                needsReward = False
                # update log
                exp_functions.logwrite([handling,j,2,0,trialClock.getTime(),globalClock.getTime(),'Forced travel',0,0],filename)
                break

        # Give reward once block is completed
        if needsReward:
            # update logs
            exp_functions.logwrite([handling,j,1,0,trialClock.getTime(),globalClock.getTime(),'Reward',0,0],filename)
            # update reward earned so far
            rewardAmount += j
            reward.setText('Trial completed \n' + 'You earned '+str(j)+' cents')
            reward.draw()
            win.flip()
            core.wait(2)

        # traveling bar
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
