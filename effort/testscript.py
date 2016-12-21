 #!/usr/bin/env python2
# -*- coding: utf-8 -*-

#Test version. The idea is to generate external trial functions and call them below in order to avoid clutter
#
#Consider:
#    - Removing the experiment handler
#    - Removing logs and using direct file output at the level of trial


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
from stroop_cond import stroop_cond
from flanker_cond import flanker_cond
from dots_cond import dots_cond
from wait_cond  import wait_cond

#### Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)


#### Store info about the experiment session
expName = 'effort'  # from the Builder filename that created this script
expInfo = {'participant':'', 'session':'001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName



#### Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s' % (expInfo['participant'], expName) #expInfo['date'])



#### An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)


#### save a log file for detail verbose info
#logFile = logging.LogFile(filename+'.log', level=logging.EXP)
#logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
endBlockNow = False # change to true if escape has been pressed during the block

### Setup the Window
win = visual.Window(
    size=(960, 600), fullscr=False, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True)

### store frame rate of monitor if we can measure it (consider removing)
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess


#### Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine


######## work block
#blockfile = open('blockselect','rb')
#work_trial = csv.reader(blockfile, delimiter=';')
#blockfile.close()

# Quit PsychoPy is escape was pressed
if endExpNow:
    core.quit()

resp_log = [] # mental_response log: 1=quit; 2=correct; 3=incorrect; 4=quit_wait; 0=miss

cond_order = [1,2,2,1,2,1,1,2,1,2,2,1,1,2,1,2]
mentalOrder = [1,2,3,1,2,3,1,2,3,1,2,3]
shuffle(mentalOrder)

# Overall condition loop
for k in cond_order:
    if k == 1:
        # mental effort block
        miss = 0
        for i in mentalOrder:
            mental_response = None
            #miss = 0
            if i == 1:
                # Calls the stroop task function with the following order of inputs: (word color, word, color on the left, color on the right, correct answer left-right, win (window),time of task)
                mental_response = stroop_cond('red','blue','red','green', 'left',win,1.5) # Pressing space returns 1, thus updating mental_response to 1 and breaking the loop
                print mental_response ## figure out how to export a value from the function that could apply here.
                message = visual.TextStim(win, text='+')
                message.draw()
                win.flip()
                core.wait(0.5)
            elif i == 2:
                # Calls the flanker task function with the following order of inputs: (flanker type, correct answer left-right, win (window),time of task)
                mental_response = flanker_cond('>><>>','left',win,1.5)
                print mental_response
                message = visual.TextStim(win, text='+')
                message.draw()
                win.flip()
                core.wait(0.5)
            elif i == 3:
                # Calls the flanker task function with the following order of inputs: (coherence, direction of dots, correct answer left (180)-right (360), win (window),time of task)
                mental_response = dots_cond(0.4,180,'left',win,1.5)
                print mental_response
                message = visual.TextStim(win, text='+')
                message.draw()
                win.flip()
                core.wait(0.5)

            ## mental_response processing
            # if space was pressed, break the loop and log it as a 1 (quit), otherwise log correct/incorrect responses onto resp_log as coded above
            if mental_response == 1:
                resp_log.append(1)
                break
            elif mental_response == 2:
                resp_log.append(2)
            elif mental_response == 3:
                resp_log.append(3)
                miss += 1

            if miss > 2:
                print miss
                break

    elif k == 2:
        # wait block
        wait_response = wait_cond(win,10)
        message = visual.TextStim(win, text='+')
        message.draw()
        win.flip()
        core.wait(0.5)
        ## wait block response processing
        #if wait_response == 1

# close Window
win.close()

# close PsychoPy
core.quit()
