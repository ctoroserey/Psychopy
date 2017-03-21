# task conditions for the mental effort foraging experiment

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


#--------------Dots-----------------------#

def dots_cond(coherDots,direcDots,corrDots,win,length):

    # Stimulus setup
    dots = visual.DotStim(
        win=win,name='dots',coherence=coherDots,dir=direcDots,nDots=100,
        dotSize=8,speed=0.003,fieldSize=1,
        fieldShape='circle',signalDots='same', noiseDots='direction',
        dotLife=1000)


    # ------Prepare to start Routine "dots"-------
    dotsClock = core.Clock()
    dotsClock.reset()  # clock
    response = 0
    taskTime = length*60

    # -------Start Routine "dots"-------
    for i in range(taskTime):
        dots.draw()
        win.flip()
    # record responses
    while response == 0:
        theseKeys = event.getKeys(keyList=['left', 'right','space','escape'])
        if len(theseKeys) == 0:
            #print 'miss'
            response = 3
        elif len(theseKeys) > 0:
            if 'escape' in theseKeys:
                core.quit()
            elif 'space' in theseKeys:
                response = 1
            elif (theseKeys[-1] == str(corrDots)) or (theseKeys[-1] == corrDots):
                #print 'correct!'
                response = 2
            else:
                #print 'incorrect'
                response = 3

    return response



#-------------Stroop-----------------#

def stroop_cond(color, word, rgbOne, rgbTwo, corrStroop, win,length):

    # Stimuli setup
    target = visual.TextStim(win=win,text=word,name='target',color=color,colorSpace='rgb',height=0.15,pos=(0,0.15));
    circleLeft = visual.Polygon(win=win,units='cm',fillColor=rgbOne,fillColorSpace='rgb',edges=1000,size=(2, 2),pos=(-4, -3))
    circleRight = visual.Polygon(win=win,units='cm',fillColor=rgbTwo,fillColorSpace='rgb',edges=1000, size=(2, 2),pos=(4, -3))


    # Prepare to start Routine "stroop"
    stroopClock = core.Clock()
    stroopClock.reset()  # clock, to be used in the future
    response = 0
    RT = 0

    # -------Start Routine "stroop"-------
    # present stimuli
    circleLeft.draw()
    circleRight.draw()
    target.draw()
    win.flip()
    core.wait(length)

    # record responses
    while response == 0:
        theseKeys = event.getKeys(keyList=['left', 'right','space','escape'])
        if len(theseKeys) == 0:
            #print 'miss'
            response = 3
        elif len(theseKeys) > 0:
            if 'escape' in theseKeys:
                core.quit()
            elif 'space' in theseKeys:
                response = 1
            elif (theseKeys[-1] == str(corrStroop)) or (theseKeys[-1] == corrStroop):
                #print 'correct!'
                response = 2
            else:
                #print 'incorrect'
                response = 3

## IMPORTANT: to return timestamps along with the answer, use a tuple like: 'return (response, RT)'
    return (response)


#--------------Flanker-----------------------#

def flanker_cond(flankType, corrFlank,win,length):

    # Stimulus setup
    flankText = visual.TextStim(win=win,text=flankType,name='flankText',height=0.15)

    # ------Prepare to start Routine "flanker"-------
    flankerClock = core.Clock()
    flankerClock.reset()  # clock, to be used in the future
    response = 0

    # -------Start Routine "flanker"-------
    # present stimuli
    flankText.draw()
    win.flip()
    core.wait(length)

    # record responses
    while response == 0:
            theseKeys = event.getKeys(keyList=['left', 'right','space','escape'])
            if len(theseKeys) == 0:
                #print 'miss'
                response = 3
            elif len(theseKeys) > 0:
                if 'escape' in theseKeys:
                    core.quit()
                elif 'space' in theseKeys:
                    response = 1
                elif (theseKeys[-1] == str(corrFlank)) or (theseKeys[-1] == corrFlank):
                    #print 'correct!'
                    response = 2
                else:
                    #print 'incorrect'
                    response = 3

    return response


#-----------------Wait----------------------#

def wait_cond(win,length):

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
    Quit_wait = event.BuilderKeyResponse() # consider deleting this and using 'response' instead
    # update component parameters for each repeat
    wait_resp = event.BuilderKeyResponse() # delete this and use 'response' instead.
    # keep track of which components have finished
    waitComponents = [waitText, wait_resp]
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
        if wait_resp.status == NOT_STARTED:
            # keep track of start time/frame for later
            wait_resp.tStart = t
            wait_resp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(wait_resp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if wait_resp.status == STARTED:
            theseKeys = event.getKeys(keyList=['space'])

            # check for experiment quit:
            if "escape" in theseKeys:
                endExpNow = True
            # check for trial quit:
            if 'space' in theseKeys:
                Quit_wait.keys = theseKeys[-1]  # just the last key pressed
                Quit_wait.rt = Quit_wait.clock.getTime()
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
