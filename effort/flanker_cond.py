def flanker_cond(flankType, corrFlank,win,length):

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

    # ------Prepare to start Routine "flanker"-------
    t = 0
    endExpNow = False # putative global quit, kept there because PsychoPy acts up when removed
    routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine
    flankerClock = core.Clock()
    flankerClock.reset()  # clock
    flankText = visual.TextStim(win=win,name='flankText',height=0.2)
    continueRoutine = True
    routineTimer.add(length)
    # update component parameters for each repeat
    flankText.setText(flankType)
    flanker_resp = event.BuilderKeyResponse()
    Quit_flank = event.BuilderKeyResponse()
    # keep track of which components have finished
    flankerComponents = [flankText, flanker_resp, Quit_flank]
    for thisComponent in flankerComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "flanker"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = flankerClock.getTime()

        # *text* updates
        if flankText.status == NOT_STARTED:
            # keep track of start time/frame for later
            #flankText.tStart = t
            flankText.setAutoDraw(True)

        # *flanker_resp* updates
        if flanker_resp.status == NOT_STARTED:
            # keep track of start time/frame for later
            flanker_resp.tStart = t
            flanker_resp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(flanker_resp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if flanker_resp.status == STARTED:
            theseKeys = event.getKeys(keyList=['left', 'right'])

            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                flanker_resp.keys = theseKeys[-1]  # just the last key pressed
                flanker_resp.rt = flanker_resp.clock.getTime()
                # was this 'correct'?
                if (flanker_resp.keys == str(corrFlank)) or (flanker_resp.keys == corrFlank):
                    flanker_resp.corr = 1
                else:
                    flanker_resp.corr = 0

        # *Quit_flank* updates
        if Quit_flank.status == NOT_STARTED:
            # keep track of start time/frame for later
            Quit_flank.tStart = t
            Quit_flank.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(Quit_flank.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if Quit_flank.status == STARTED:
            theseKeys = event.getKeys(keyList=['space'])

            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                Quit_flank.keys = theseKeys[-1]  # just the last key pressed
                Quit_flank.rt = Quit_flank.clock.getTime()
                # a response ends the routine
                continueRoutine = False

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in flankerComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "flanker"-------
    for thisComponent in flankerComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    #if flanker_resp.keys in ['', [], None]:  # No response was made
    #    flanker_resp.keys=None
    #    # was no response the correct answer?!
    #    if str(corrFlank).lower() == 'none':
    #       flanker_resp.corr = 1  # correct non-response
    #    else:
    #       flanker_resp.corr = 0  # failed to respond (incorrectly)
    ## store data for thisExp (ExperimentHandler)
    #thisExp.addData('flanker_resp.keys',flanker_resp.keys)
    #thisExp.addData('flanker_resp.corr', flanker_resp.corr)
    #if flanker_resp.keys != None:  # we had a response
    #    thisExp.addData('flanker_resp.rt', flanker_resp.rt)
    #thisExp.nextEntry()
    ## check responses
    #if Quit_flank.keys in ['', [], None]:  # No response was made
    #    Quit_flank.keys=None
    #thisExp.addData('Quit_flank.keys',Quit_flank.keys)
    #if Quit_flank.keys != None:  # we had a response
    #    thisExp.addData('Quit_flank.rt', Quit_flank.rt)
    #thisExp.nextEntry()
