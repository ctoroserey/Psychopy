# wtw experiment helper module

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, event, core
import numpy as np
import csv
import threading
import Queue
import wtw.drawSample
import wtw.detectResponse
import wtw.handgrip


######################################
# display a simple instruction message
def showMessage(win,msgObject,msgText):
    msgObject.setText(msgText)
    continueRoutine = True
    msgObject.setAutoDraw(True)
    win.flip()
    core.wait(1, hogCPUperiod=0) # do not accept keypress for the first 1 s
    event.waitKeys()
    msgObject.setAutoDraw(False)


#######################################################
# load a systematically randomized counterbalance index
def getCBal(nCbalCells):
    # will return an index in range(nCbalCells)
    # try loading the cbal queue
    csvfname = 'cbal.csv'
    cbArray = np.array([])
    try:
        with open(csvfname, 'r') as csvfile:
            cr = csv.reader(csvfile)
            cbArray = cr.next() # only 1 row
            cbArray = np.array(cbArray,dtype='int')
    except:
        pass
    # if cbArray is empty, generate one with 2 instances of each cell
    if cbArray.size == 0:
        cbArray = np.repeat(range(nCbalCells),2)
        np.random.shuffle(cbArray)
    # pop the first item from the list
    cbalIdx = cbArray[0]
    cbArray = np.delete(cbArray,0)
    # save the list and return the current index
    with open(csvfname, 'w') as csvfile:
        cw = csv.writer(csvfile)
        cw.writerow(cbArray)
    return cbalIdx


####################
# initialize stimuli
def createStimulusObjects(win,frameDur):

    # set some colors
    tokenRewardColor = [0, 0, 1]
    tokenHoleColor = [-0.2, -0.2, -0.2]

    # instructions text
    message = visual.TextStim(win=win, ori=0, name='message', text=u'Please press a key to begin.',
        font=u'Arial', pos=[0, 0], height=0.05, wrapWidth=1.2, color=u'white', colorSpace='rgb',
        alignHoriz='center')

    # circular token
    token = visual.Circle(win=win, radius=0.1, edges=64, units='height',
        lineWidth=2, lineColor=[1,1,1], fillColor=[0,0,0], pos=(0, 0), interpolate=True,
        name='token')

    # text with token value
    tokenText = visual.TextStim(win=win, ori=0, name='tokenText',
        text='0',    font=u'Arial', units='height',
        pos=[0, 0], height=0.05, wrapWidth=None,
        color=[1,1,1], colorSpace='rgb', opacity=1, depth=0.0)

    # 'ready' text on the token
    readyText = visual.TextStim(win=win, ori=0, name='readyText',
        text='Grip!',    font=u'Arial', units='height',
        pos=[0, 0], height=0.03, wrapWidth=None,
        color=[1,1,1], colorSpace='rgb', opacity=1, depth=0.0)

    # text for "SOLD"
    soldText = visual.TextStim(win=win, ori=0, name='soldText',
        text='SOLD',    font=u'Arial', units='height',
        pos=[0, 0], height=0.15, wrapWidth=None,
        color=[1,-0.5,-0.5], colorSpace='rgb', opacity=1, depth=0.0)

    # progress bar
    progBarMaxTime = 30 # in s
    progBarMaxLength = 0.5 # in screen height units
    progBarVertPos = -0.2 # will need this when updating the position
    progressBar = visual.Rect(win=win, units='height', pos=(0,progBarVertPos),
        width=1, height=0.05, fillColor=[1,1,1], name='progressBar', autoLog=False)

    # progress bar base
    baseN = progBarVertPos + 0.03
    baseS = progBarVertPos - 0.03
    baseE = -0.25 + 0.015
    baseW = -0.25 - 0.005
    baseVerts = ((baseE, baseN), (baseW, baseN), (baseW, baseS), (baseE, baseS))  # NE, NW, SW, SE
    progressBarBase = visual.ShapeStim(win=win, units='height', vertices=baseVerts, closeShape=False,
        lineColor=[-0.2, -0.2, -0.2], lineWidth=5, name='progressBarBase')

    # time left text: TextStim version
    # slow to update; tend to get skipped frames at whole numbers of seconds
    timeLeftText = visual.TextStim(win=win, ori=0,
        text='Time left', font=u'Arial', units='height',
        pos=[-0.1, -0.3], height=0.03, wrapWidth=None,
        color=[1,1,1], alignHoriz='left', autoLog=False, name='timeLeftText')

    # total earned text: TextStim version
    totalEarnedText = visual.TextStim(win=win, ori=0,
        text='Total earned: $0.00', font=u'Arial', units='height',
        pos=[-0.1, -0.35], height=0.03, wrapWidth=None,
        color=[1,1,1], alignHoriz='left', name='totalEarnedText')

    # grip force meter
    meterDial = visual.Circle(win=win, radius=0.1, units='height',
        fillColor=[-0.5, -0.5, -0.5], pos=[0, 0], name='meterDial')
    meterMarker = visual.Line(win=win, start=(0,0.05), end=(0,0.1), units='height',
        lineColor=[1, 1, 1], lineWidth=2, name='meterMarker')
    meterNeedle = visual.ShapeStim(win=win, vertices=((0,0.09), (0.01,-0.02), (-0.01,-0.02)),
        units='height', fillColor=[1,0,0], lineColor=[1,0,0], pos=(0, 0), autoLog=False, name='meterNeedle')
    meterDial.size *= 1 # resize all meter components
    meterMarker.size *= 1
    meterNeedle.size *= 1

    return {'message':message, 'token':token, 'tokenText':tokenText, 'readyText':readyText, 'soldText':soldText,
        'progressBar':progressBar, 'progressBarBase':progressBarBase, 'timeLeftText':timeLeftText,
        'totalEarnedText':totalEarnedText,'progBarMaxTime':progBarMaxTime,
        'progBarMaxLength':progBarMaxLength, 'tokenRewardColor':tokenRewardColor,
        'tokenHoleColor':tokenHoleColor, 'frameDur':frameDur, 'meterDial':meterDial,
        'meterMarker':meterMarker, 'meterNeedle':meterNeedle}


###########################
# present a block of trials
def showTrials(blockParams, stimObjects, thisExp, expObjects):

    # unpack inputs from blockParams
    trialLimit = blockParams['trialLimit']

    # unpack inputs from stimObjects
    frameDur = stimObjects['frameDur']
    readyText = stimObjects['readyText'] # Claudio: could change this to display the prospective reward.
    meterDial = stimObjects['meterDial']
    meterMarker = stimObjects['meterMarker']
    meterNeedle = stimObjects['meterNeedle']

    # unpack inputs from expObjects
    win = expObjects['win']
    trialClock = core.Clock()
    keySH = expObjects['keySH']
    LabJack = expObjects['LabJack'] # will be 0 if not connected
    handgripNeeded = expObjects['handgripNeeded']
    threshold = expObjects['thresholdGripStrength']
    calibLevel = expObjects['calibLevel']

    # initialize variables
    stateNow = 'iti'
    nextEventTime = 0.5 # brief gap before the first token
        # the gap is so that in the "hold down spacebar" condition, the keypress to
        # terminate the instruction screen does not result in skipping the "Ready" state

    # initial state of the display
    if handgripNeeded: # display the force meter. Claudio: IMPORTANT
        meterDial.setAutoDraw(True)
        meterMarker.setAutoDraw(True)
        meterNeedle.setAutoDraw(True)

    # package arguments to pass to the response collection function
    respArgs = {'blockClock':trialClock, 'keySH':keySH, 'threshold':threshold}

    # write marker channel for block onset (if applicable)
    # marker voltage steps to 1 volt
    # Claudio: put it on the main script?
    if LabJack != 0:
        LabJack.streamStart()
        streamObj = LabJack.streamData()
        wtw.handgrip.startBlockSignal(LabJack)
    else:
        streamObj = False
        
    # if needed, start a separate thread to monitor handgrip inputs
    if handgripNeeded:
        hgQueue = Queue.LifoQueue() # create a queue
        readStream = threading.Event() # create an event
        readStream.set()
        t = threading.Thread(target=wtw.handgrip.streamReader,args=(readStream,streamObj,hgQueue))
        t.start()
        respArgs['hgQueue'] = hgQueue # to pass to response collection functions

    # reset clock
    trialClock.reset()

    # Claudio: basic response output
    response = 0

    # while loop for the duration of the trial
    # events are controlled by the trial 'state,' a text string that progresses as follows:
    #   'iti' [optionally to 'ready'] to 'waiting' [optionally to 'matured'] to 'feedback' to 'iti'
    while (trialClock.getTime() < trialLimit): #(responseOutput['responded'] == False): #

        # clock time for this iteration
        timeNow = trialClock.getTime()

        # always check for a sell response
        responseOutput = wtw.detectResponse.releaseHandGrip(respArgs) #checkSellResponse(respArgs)
        respArgs = responseOutput['respArgs']

        # changes in and out of the pre-trial 'ready' state
        if (stateNow == 'iti') and (timeNow >= (nextEventTime - frameDur)) and responseOutput['responded']:
            # enter 'ready' if it's time to start a new trial but the sell response is active,
            # meaning the new trial would go straight to 'feedback'
            stateNow = 'ready'
            readyText.setAutoDraw(True)
            ##################
            if LabJack != 0:
                wtw.handgrip.trialOnsetSignal(LabJack)
            ##################

        if (stateNow == 'ready') and responseOutput['responded']:
            # if we were in 'ready' and now the sell response is no longer active; ok to start
            if timeNow > 1:
                response = 1
                break
        elif (stateNow == 'ready') and not responseOutput['responded']:
            stateNow = 'iti' # will trigger the conditional below for 'iti' -> 'waiting'
            nextEventTime = timeNow # time spent in 'ready' is not deducted from the delay
            readyText.setAutoDraw(False)

        # time-dependent state changes
        # state change from iti to waiting (new trial onset)
        if (stateNow == 'iti') and (timeNow >= (nextEventTime - frameDur)):
            stateNow = 'waiting'
            event.clearEvents() # ITI key presses, if any, should not carry over

            #################################
            # Claudio: Might have to put this back. In my case it only makes sense at the beginning, though
            # if using LabJack, signal trial onset
            # step up marker channel to 3 volts
            if LabJack != 0:
                wtw.handgrip.trialOnsetSignal(LabJack)
            #################################

        # response-dependent state change (from waiting or matured to feedback)
        if stateNow in ['waiting', 'matured']:

            # if a sell response was recorded. Claudio: if quit
            if (responseOutput['responded'] == True):

                # if using LabJack, signal trial end
                # step down marker channel to 1 volt
                if LabJack != 0:
                    wtw.handgrip.trialEndSignal(LabJack)

                # I only need the response, everything else is logged from the main script.
                response = 1
                break

        # update force meter if applicable
        if handgripNeeded:
            gripForce = responseOutput['gripForce'] # analog output from the response detection call above
            calibFloor = calibLevel['relax']
            # get current force as a fraction of the threshold
            gripForceFrac = (gripForce - calibFloor) / (threshold - calibFloor)
            gripForceFrac = np.max([gripForceFrac, 0]) # set a low bound at zero
            gripForceFrac = np.min([gripForceFrac, 2]) # high bound at twice the threshold
            meterAngle = 135 * (gripForceFrac - 1)
            meterNeedle.ori = meterAngle


        # flip the display
        # note: output of progressBar.verticesPix changes on each iteration, so
        # we always flip.
        win.flip()

        # check for quit (the Esc key)
        if event.getKeys(keyList=["escape"]):
            if handgripNeeded:
                readStream.clear() # close the thread
                t.join() # wait for the thread to close
            if LabJack != 0: # close the DAQ stream if applicable
                wtw.handgrip.stopBlockSignal(LabJack)  # step down marker voltage to 0 volts
                LabJack.streamStop()
                LabJack.close()
            core.quit()

        # end of while loop within a block

    # at the end of the block, remove all visual objects
    readyText.setAutoDraw(False)
    meterDial.setAutoDraw(False)
    meterMarker.setAutoDraw(False)
    meterNeedle.setAutoDraw(False)

    # close the DAQ stream if applicable
    if handgripNeeded:
        readStream.clear() # close the thread
        t.join() # wait for the thread to close
    #####################
    if LabJack != 0:
        wtw.handgrip.stopBlockSignal(LabJack)  # step down marker voltage to 0 volts
        LabJack.streamStop()
    #####################
    if LabJack != 0:
        wtw.handgrip.trialEndSignal(LabJack)

    # output response
    return response #trialOutput # once it's ready, use return response for the foraging script
