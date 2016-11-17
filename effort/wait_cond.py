def wait_cond(win,length):

# To do:
#    - find out how to log the data properly, and trim further
#    - Modify so it just waits


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

    # Stimulus
    waitText = visual.TextStim(win=win,name='+',height=0.2)

    # ------Prepare to start Routine "waiter"-------
    t = 0
    endExpNow = False # putative global quit, kept there because PsychoPy acts up when removed
    routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine
    waiterClock = core.Clock()
    waiterClock.reset()  # clock
    continueRoutine = True
    routineTimer.add(length)
    # update component parameters for each repeat
    Quit_wait = event.BuilderKeyResponse() # delete this and use 'response' instead.
    # keep track of which components have finished
    waiterComponents = [waitText, waiter_resp, Quit_wait]
    for thisComponent in waiterComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "waiter"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = waiterClock.getTime()

        # show text
        if waitText.status == NOT_STARTED:
            waitText.setAutoDraw(True)

        # response check
        if waiter_resp.status == NOT_STARTED:
            # keep track of start time/frame for later
            waiter_resp.tStart = t
            waiter_resp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(waiter_resp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if waiter_resp.status == STARTED:
            theseKeys = event.getKeys(keyList=['left', 'right','space'])

            # check for experiment quit:
            if "escape" in theseKeys:
                endExpNow = True
            # check for trial quit:
            if 'space' in theseKeys:
                Quit_wait.keys = theseKeys[-1]  # just the last key pressed
                Quit_wait.rt = Quit_wait.clock.getTime()
                continueRoutine = False
            # if not quit, then record response
            elif len(theseKeys) > 0:  # at least one key was pressed
                waiter_resp.keys = theseKeys[-1]  # just the last key pressed
                # was this 'correct'?
                if (waiter_resp.keys == str(corrwait)) or (waiter_resp.keys == corrwait):
                    waiter_resp.corr = 1
                else:
                    waiter_resp.corr = 0

        # a component has requested a forced-end of Routine
        if not continueRoutine:
            break
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "waiter"-------
    # makes sure all the stimuli stop showing
    for thisComponent in waiterComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)



    # check responses
    #if waiter_resp.keys in ['', [], None]:  # No response was made
    #    waiter_resp.keys=None
    #    # was no response the correct answer?!
    #    if str(corrwait).lower() == 'none':
    #       waiter_resp.corr = 1  # correct non-response
    #    else:
    #       waiter_resp.corr = 0  # failed to respond (incorrectly)
    ########

    ## store data for thisExp (ExperimentHandler)
    #thisExp.addData('waiter_resp.keys',waiter_resp.keys)
    #thisExp.addData('waiter_resp.corr', waiter_resp.corr)
    #if waiter_resp.keys != None:  # we had a response
    #    thisExp.addData('waiter_resp.rt', waiter_resp.rt)
    #thisExp.nextEntry()
    ## check responses
    #if Quit_wait.keys in ['', [], None]:  # No response was made
    #    Quit_wait.keys=None
    #thisExp.addData('Quit_wait.keys',Quit_wait.keys)
    #if Quit_wait.keys != None:  # we had a response
    #    thisExp.addData('Quit_wait.rt', Quit_wait.rt)
    #thisExp.nextEntry()
