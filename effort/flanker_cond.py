def flanker_cond(flankType, corrFlank,win,length):

# To do:
#    - find out how to log the data properly, and trim further
#    - remove Quit_flank
#    - Trim further 

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
    flankText = visual.TextStim(win=win,name='flankText',height=0.2)

    # ------Prepare to start Routine "flanker"-------
    t = 0
    endExpNow = False # putative global quit, kept there because PsychoPy acts up when removed
    routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine
    flankerClock = core.Clock()
    flankerClock.reset()  # clock
    continueRoutine = True
    routineTimer.add(length)
    # update component parameters for each repeat
    flankText.setText(flankType)
    flanker_resp = event.BuilderKeyResponse()
    Quit_flank = event.BuilderKeyResponse() # delete this and use 'response' instead.
    # keep track of which components have finished
    flankerComponents = [flankText, flanker_resp, Quit_flank]
    for thisComponent in flankerComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "flanker"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = flankerClock.getTime()

        # show text
        if flankText.status == NOT_STARTED:
            flankText.setAutoDraw(True)

        # response check
        if flanker_resp.status == NOT_STARTED:
            # keep track of start time/frame for later
            flanker_resp.tStart = t
            flanker_resp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(flanker_resp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if flanker_resp.status == STARTED:
            theseKeys = event.getKeys(keyList=['left', 'right','space'])

            # check for experiment quit:
            if "escape" in theseKeys:
                endExpNow = True
            # check for trial quit:
            if 'space' in theseKeys:
                Quit_flank.keys = theseKeys[-1]  # just the last key pressed
                Quit_flank.rt = Quit_flank.clock.getTime()
                continueRoutine = False
            # if not quit, then record response
            elif len(theseKeys) > 0:  # at least one key was pressed
                flanker_resp.keys = theseKeys[-1]  # just the last key pressed
                # was this 'correct'?
                if (flanker_resp.keys == str(corrFlank)) or (flanker_resp.keys == corrFlank):
                    flanker_resp.corr = 1
                else:
                    flanker_resp.corr = 0

        # a component has requested a forced-end of Routine
        if not continueRoutine:
            break
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "flanker"-------
    # makes sure all the stimuli stop showing
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
    ########

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
