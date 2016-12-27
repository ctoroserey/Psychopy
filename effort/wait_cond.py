def wait_cond(win,length):

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


    # Stimulus Setup
    waitText = visual.TextStim(win=win,name='+',text='+',height=0.1)

    # Stimulus
    waitText = visual.TextStim(win=win,name='+',text='+',height=0.2)


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
