# task conditions for the mental effort foraging experiment

""" Consider:
    -   Adding ISI to task functions (currently in the big script)
    -   Trim the wait condition. It works, but it's ugly
    """

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

#---------------Log writing---------#

def logwrite(values,filename,**new_directory):
    # Appends a new row 'values' to filename_log.csv
    # Optional (*directory): write log in a non-current path by adding newPath = 'desired path'
    # File will be created in pwd unless 'filename' contains path info or newPath is called

    if 'newPath' in new_directory:
        print 'new path selected: ' + new_directory['newPath']
        filename = os.path.join(new_directory['newPath'],filename)

    with open(filename+'_log.csv','a') as logfile:
        logwriter = csv.writer(logfile, delimiter=',')
        logwriter.writerow(values)
    logfile.close()


#--------------Dots-----------------------#

def dotsCondition(coherDots,direcDots,corrDots,win,length):

    # Stimulus setup
    dots = visual.DotStim(
        win=win,name='dots',coherence=coherDots,dir=direcDots,nDots=100,
        dotSize=8,speed=0.003,fieldSize=1,
        fieldShape='circle',signalDots='same', noiseDots='direction',
        dotLife=1000)


    # ------Prepare to start Routine "dots"-------
    dotsClock = core.Clock()
    response = 0
    RT = 0
    taskTime = length*60

    # -------Start Routine "dots"-------
    for i in range(taskTime):
        dots.draw()
        win.flip()
        theseKeys = event.getKeys(keyList=['left', 'right','space','escape'])
        if len(theseKeys) > 0:
            if 'escape' in theseKeys: # quit experiment
                core.quit()
            elif 'space' in theseKeys: # quit trial
                response = 1
                RT = dotsClock.getTime()
                break
            elif (theseKeys[-1] == str(corrDots)) or (theseKeys[-1] == corrDots): # correct
                response = 2
                RT = dotsClock.getTime()
            else: # incorrect
                response = 3
                RT = dotsClock.getTime()
    if response==0:
        response = 3
        RT = dotsClock.getTime()
    # record responses
    return response, RT



#-------------Stroop-----------------#

def stroopCondition(color, word, rgbOne, rgbTwo, corrStroop, win,length):

    # Stimuli setup
    target = visual.TextStim(win=win,text=word,name='target',color=color,colorSpace='rgb',height=0.15,pos=(0,0.15));
    circleLeft = visual.Polygon(win=win,units='cm',fillColor=rgbOne,fillColorSpace='rgb',edges=1000,size=(2, 2),pos=(-4, -3))
    circleRight = visual.Polygon(win=win,units='cm',fillColor=rgbTwo,fillColorSpace='rgb',edges=1000, size=(2, 2),pos=(4, -3))


    # Prepare to start Routine "stroop"
    stroopClock = core.Clock()
    response = 0
    RT = 0

    # -------Start Routine "stroop"-------
    # present stimuli
    circleLeft.setAutoDraw(True)
    circleRight.setAutoDraw(True)
    target.setAutoDraw(True)
    win.flip()

    # record responses
    while stroopClock.getTime() < length:
        theseKeys = event.getKeys(keyList=['left', 'right','space','escape'])
        if len(theseKeys) > 0:
            if 'escape' in theseKeys: # quit experiment
                core.quit()
            elif 'space' in theseKeys: # quit trial
                response = 1
                RT = stroopClock.getTime()
                break
            elif (theseKeys[-1] == str(corrStroop)) or (theseKeys[-1] == corrStroop): # correct
                response = 2
                RT = stroopClock.getTime()
            else: # incorrect
                response = 3
                RT = stroopClock.getTime()

    circleLeft.setAutoDraw(False)
    circleRight.setAutoDraw(False)
    target.setAutoDraw(False)

    if response==0:
        response = 3
        RT = stroopClock.getTime()

    return response, RT


#--------------Flanker-----------------------#

def flankerCondition(flankType, corrFlank,win,length):

    # Stimulus setup
    flankText = visual.TextStim(win=win,text=flankType,name='flankText',height=0.15)

    # ------Prepare to start Routine "flanker"-------
    flankerClock = core.Clock()
    response = 0
    RT = 0

    # -------Start Routine "flanker"-------
    # present stimuli
    flankText.setAutoDraw(True)
    win.flip()

    # record responses
    while flankerClock.getTime() < length: #response == 0:
            theseKeys = event.getKeys(keyList=['left', 'right','space','escape'])
            if len(theseKeys) > 0:
                if 'escape' in theseKeys: # quit experiment
                    core.quit()
                elif 'space' in theseKeys: # quit
                    response = 1
                    RT = flankerClock.getTime()
                    break
                elif (theseKeys[-1] == str(corrFlank)) or (theseKeys[-1] == corrFlank): # correct
                    response = 2
                    RT = flankerClock.getTime()
                else: # incorrect
                    response = 3
                    RT = flankerClock.getTime()

    flankText.setAutoDraw(False)

    if response==0:
        response = 3
        RT = flankerClock.getTime()

    return response, RT


#-----------------Wait----------------------#

def waitCondition(win,length):

    """ This can be trimmed a good amount """

    # Stimulus Setup
    waitText = visual.TextStim(win=win,name='+',text='+',height=0.1)

    # ------Prepare to start Routine "wait"-------
    t = 0
    endExpNow = False # putative global quit, kept there because PsychoPy acts up when removed
    routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine
    waitClock = core.Clock()
    waitClock.reset()  # clock
    continueRoutine = True
    routineTimer.add(length)
    quitWait = event.BuilderKeyResponse() # consider deleting this and using 'response' instead
    # update component parameters for each repeat
    waitResponse = event.BuilderKeyResponse() # delete this and use 'response' instead.
    # keep track of which components have finished
    waitComponents = [waitText, waitResponse]
    for thisComponent in waitComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    response = 0
    # -------Start Routine "wait"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = waitClock.getTime()

        # show text
        if waitText.status == NOT_STARTED:
            waitText.setAutoDraw(True)

        # response check
        if waitResponse.status == NOT_STARTED:
            # keep track of start time/frame for later
            waitResponse.tStart = t
            waitResponse.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(waitResponse.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if waitResponse.status == STARTED:
            theseKeys = event.getKeys(keyList=['space'])

            # check for experiment quit:
            if "escape" in theseKeys:
                endExpNow = True
            # check for trial quit:
            if 'space' in theseKeys:
                quitWait.keys = theseKeys[-1]  # just the last key pressed
                quitWait.rt = quitWait.clock.getTime()
                continueRoutine = False
            # figure out the best way to record responses

        # a component has requested a forced-end of Routine
        if not continueRoutine:
            response = 1
            for thisComponent in waitComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            return response
            break
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "wait"-------
    # makes sure all the stimuli stop showing
    for thisComponent in waitComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
