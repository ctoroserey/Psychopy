 #!/usr/bin/env python2
# -*- coding: utf-8 -*-

""" Given that there are 4 iti blocks, a 10 min session will require each session to be ~2.5 mins (150s)"""

from __future__ import absolute_import, division
from psychopy import locale_setup, gui, visual, core, data, event, logging, sound
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding
import csv
import time
from wait_cond  import wait_cond
from random import randint


##------------------------ Basic experiment settings -------------------------
#### Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

#### Store info about the experiment session
expName = 'waitTask'  # from the Builder filename that created this script
expInfo = {'participant':'', 'session':'001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = time.strftime("%d%m%Y")#data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

#### Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

### Setup the Window
win = visual.Window(
    size=(2560,1440), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True)

### store frame rate of monitor if we can measure it (consider removing)
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess



##-------------------- Setting up stimuli, etc. ----------------------------
## Reward stimulus
reward = visual.TextStim(win,height=0.1,text='$0.25')
## Traveling stimuli
traveling = visual.TextStim(win, text='Traveling',height=0.1,pos=(0.0,0.15)) # Just the text
travel1 = visual.Rect(win=win,height=0.1,width=0.1,lineWidth=2,lineColor='white') # Bar borders (width=((set_iti*60)/1000))
travel2 = visual.Rect(win=win,height=0.1,width=0.1, fillColor='green') # Green progress bar
## ISI stimulus
isi = visual.TextStim(win, text='+')
## ITI cue stimulus
iti = visual.TextStim(win=win,text='Travel time = x seconds',height=0.1,pos=(0.0,0.15))
## Cummulative reward amount
reward_amount = 0
## task lengths
length = 1.5 # for each mental task
wait_length = 10 # for the waiting block
blockLength = 150 # how long in seconds each iti block will be
## Log aggregators, output as csv
iti_log = [] # what iti block we're in
rwd_log = [] # current reward opportunity
deci_log = [] # did they complete (1), quit (2), or fail (3) the block
rt_log = [] # within-trial time of decision/completion
totime_log = [] # absolute time throughout the experimental session

### Order of the conditions and the mental tasks
iti_order = [1,1,3,3,5,5,8,8]
shuffle(iti_order)
rewardOrder = [0.05,0.05,0.15,0.15,0.25,0.25]

##----------------------- Begin experiment ---------------------------------

# initial window, waits for input to begin the experiment
start = visual.TextStim(win, text='Remember: respond with the left or right keys \n' + 'Press space to quit each condition \n'+'Press ENTER to begin',height=0.06)
start.draw()
win.flip()
event.waitKeys(keyList=['return'])

globalClock = core.Clock()  # to track the time since experiment started

##----------------------- Overall condition loop ---------------------------

for k in iti_order:
    # ITI cue
    isi.draw()
    win.flip()
    core.wait(1)
    iti.setText('Travel time ='+' '+str(k)+' '+'seconds')
    travel1.setWidth((k*60)/1000)
    travel1.setFillColor('green')
    iti.draw()
    travel1.draw()
    win.flip()
    core.wait(4)
    travel1.setFillColor(None) # otherwise the bar will just be invariant below
    # track how long each iti block is (e.g. 2.5 mins each for a 10 min session)
    itiClock = core.Clock()
    counter = 0 # to help distribute rewards more evenly
    # Begin trials
    while itiClock.getTime() < blockLength:
        if counter == 0:
            shuffle(rewardOrder)
        j = rewardOrder[counter]
        needs_reward = True # changes to False if the participant quits the block
        blockClock = core.Clock() # sets a timer for the trial
        message = visual.TextStim(win, text=' Next reward = $'+str(j), height=0.1)
        message.draw()
        win.flip()
        core.wait(2)
        if event.getKeys(keyList=['escape']): #this syntax can be used in the future in case we want to allow quitting during cues
            core.quit()
        # Calls the wait block function, wait_length = length of block
        wait_response = wait_cond(win,wait_length)

        ## Wait block response processing
        if wait_response == 1: # if quit
            needs_reward = False
            # update logs
            iti_log.append(k)
            rwd_log.append(j)
            deci_log.append(2)
            rt_log.append(str(blockClock.getTime()))
            totime_log.append(str(globalClock.getTime()))
        else:
            # Give reward once block is completed
            # update logs
            iti_log.append(k)
            rwd_log.append(j)
            deci_log.append(1)
            rt_log.append(str(blockClock.getTime()))
            totime_log.append(str(globalClock.getTime()))
            # update the reward earned so far
            reward_amount += j
            reward.setText('You earned $'+str(j))
            reward.draw()
            win.flip()
            core.wait(2)

        # ITI (traveling)
        travel1.setWidth((k*60)/1000)
        travel1.setAutoDraw(True)
        traveling.setAutoDraw(True)
        win.flip()
        for i in range(k*60):
            travel2.setWidth(i/1000)
            travel2.draw()
            win.flip()
        traveling.setAutoDraw(False)
        travel1.setAutoDraw(False)

        if counter == 5:
            counter = 0
        else:
            counter += 1

## log writting on csv file
with open(filename+'_log.csv','wb') as logfile:
    logwriter = csv.writer(logfile, delimiter=',')
    logwriter.writerow(('ITI','Expected Reward','Decision (1=complete; 2=quit; 3=failed)','RT','Total Time'))
    for i in range(len(iti_log)):
        logwriter.writerow((iti_log[i],rwd_log[i],deci_log[i],rt_log[i],totime_log[i]))
    logwriter.writerow(('Total reward = $',reward_amount))
logfile.close()

## Final screen showing final reward amount
start = visual.TextStim(win, text='Great work! You earned $' + str(reward_amount),height=0.08)
start.draw()
win.flip()
event.waitKeys(keyList=['return'])

# close Window
win.close()

# close PsychoPy
core.quit()
