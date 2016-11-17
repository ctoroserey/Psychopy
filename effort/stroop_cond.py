def stroop_cond(color, word, rgbOne, rgbTwo, corrStroop, win,length):

    ### I don't get GitHub
    ### See if these imports can be done globally. In any case, the overhead is negligible.
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

    #globalClock = core.Clock()  # to track the time since experiment started
    routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine
    stroopClock = core.Clock()
    target = visual.TextStim(win=win,name='target',height=0.2);
    circleLeft = visual.Polygon(win=win,units='cm',edges=1000,size=(2, 2),pos=(-4, -4))
    circleRight = visual.Polygon(win=win,units='cm',edges=1000, size=(2, 2),pos=(4, -4))

    # ------Prepare to start Routine "stroop"-------

    t = 0
    stroopClock.reset()  # clock
    continueRoutine = True
    routineTimer.add(length)
    # update component parameters for each repeat
    target.setColor(color, colorSpace='rgb')
    target.setText(word)
    response = event.BuilderKeyResponse()
    circleLeft.setFillColor(rgbOne)
    circleRight.setFillColor(rgbTwo)
    Quit_stroop = event.BuilderKeyResponse()
    # keep track of which components have finished
    stroopComponents = [target, response, circleLeft, circleRight, Quit_stroop]
    for thisComponent in stroopComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "stroop"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        endTrialNow = False
        t = stroopClock.getTime()

        if circleLeft.status == NOT_STARTED:
            circleLeft.setAutoDraw(True)
            circleRight.setAutoDraw(True)
            target.setAutoDraw(True)

        # *response* updates
        if response.status == NOT_STARTED:
            response.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(response.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
            theseKeys = event.getKeys(keyList=['left', 'right', 'space'])

            # check for quit:
            if "space" in theseKeys:
                response.rt = response.clock.getTime()
                continueRoutine = False
                #endTrialNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                response.keys = theseKeys[-1]  # just the last key pressed
                # was this 'correct'?
                if (response.keys == str(corrStroop)) or (response.keys == corrStroop):
                    response.corr = 1 # Find out how to export this value. Maybe into an excel spreadsheet?
                else:
                    response.corr = 0


        # *Quit_stroop* updates
        if Quit_stroop.status == NOT_STARTED:
            # keep track of start time/frame for later
            Quit_stroop.tStart = t
            Quit_stroop.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(Quit_stroop.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if Quit_stroop.status == STARTED:
            theseKeys = event.getKeys(keyList=['space'])
            # check for quit:
            if "space" in theseKeys:
                endTrialNow = True
                Quit_stroop.keys = theseKeys[-1]  # just the last key pressed
                Quit_stroop.rt = Quit_stroop.clock.getTime()
                # a response ends the routine
                continueRoutine = False


        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "stroop"-------
    # makes sure all the stimuli stop showing
    for thisComponent in stroopComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)



    # check responses
    #if response.keys in ['', [], None]:  # No response was made
    #    response.keys=None
    #    # was no response the correct answer?!
    #    if str(corrStroop).lower() == 'none':
    #       response.corr = 1  # correct non-response
    #    else:
    #       response.corr = 0  # failed to respond (incorrectly)
    ########

    # store data for thisExp (ExperimentHandler)
    #thisExp.addData('response.keys',response.keys)
    #thisExp.addData('response.corr', response.corr)
    #if response.keys != None:  # we had a response
    #    thisExp.addData('response.rt', response.rt)
    #thisExp.nextEntry()
    ## check responses
    #if Quit_stroop.keys in ['', [], None]:  # No response was made
    #    Quit_stroop.keys=None
    #thisExp.addData('Quit_stroop.keys',Quit_stroop.keys)
    #    if Quit_stroop.keys != None:  # we had a response
    #    thisExp.addData('Quit_stroop.rt', Quit_stroop.rt)
    #thisExp.nextEntry()
