def stroop_cond(color, word, rgbOne, rgbTwo, corrStroop, win,length):

# To do:
#    - find out how to log the data properly, and trim further
#    - remove Quit_stroop
#    - Trim further

    ### I don't get GitHub
    ### Or maybe...
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


    # Stimuli
    target = visual.TextStim(win=win,name='target',height=0.2);
    circleLeft = visual.Polygon(win=win,units='cm',edges=1000,size=(2, 2),pos=(-4, -4))
    circleRight = visual.Polygon(win=win,units='cm',edges=1000, size=(2, 2),pos=(4, -4))

    # this global variable quits the mental effort block if = 1
    global quit_block

    # ------Prepare to start Routine "stroop"-------

    t = 0
    endExpNow = False # putative global quit, kept there because PsychoPy acts up when removed
    routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine
    stroopClock = core.Clock()
    stroopClock.reset()  # clock
    continueRoutine = True
    routineTimer.add(length)
    # update component parameters for each repeat
    target.setColor(color, colorSpace='rgb')
    target.setText(word)
    stroop_resp = event.BuilderKeyResponse()
    circleLeft.setFillColor(rgbOne)
    circleRight.setFillColor(rgbTwo)
    Quit_stroop = event.BuilderKeyResponse() # delete this and use 'response' instead.
    # keep track of which components have finished
    stroopComponents = [target, stroop_resp, circleLeft, circleRight, Quit_stroop]
    for thisComponent in stroopComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    response = 0
    # -------Start Routine "stroop"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = stroopClock.getTime()

        # show stimuli
        if circleLeft.status == NOT_STARTED:
            circleLeft.setAutoDraw(True)
            circleRight.setAutoDraw(True)
            target.setAutoDraw(True)

        # response check
        if stroop_resp.status == NOT_STARTED:
            stroop_resp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(stroop_resp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if stroop_resp.status == STARTED:
            theseKeys = event.getKeys(keyList=['left', 'right','space'])

            # check for experiment quit:
            if "escape" in theseKeys:
                endExpNow = True
            # check for trial quit:
            if 'space' in theseKeys:
                #Quit_stroop.keys = theseKeys[-1]  # just the last key pressed
                #Quit_stroop.rt = Quit_stroop.clock.getTime()
                continueRoutine = False

            # if not quit, then record response
            elif len(theseKeys) > 0:  # at least one key was pressed
                stroop_resp.keys = theseKeys[-1]  # just the last key pressed
                # was this 'correct'?
                if (stroop_resp.keys == str(corrStroop)) or (stroop_resp.keys == corrStroop):
                    print 'correct!'
                    stroop_resp.corr = 1
                    response = 2
                #elif (stroop_resp.keys is not str(corrStroop)) or (stroop_resp.keys is not corrStroop):
                #    stroop_resp.corr = 0
                #    response = 3
            else: # no response
                response = 3

        # a component has requested a forced-end of Routine
        if not continueRoutine:
            response = 1            # if not quit, then record response
            for thisComponent in stroopComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            return response
            break
        # ends experiment if escape has been pressed
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()


    # -------Ending Routine "stroop"-------
    # makes sure all the stimuli stop showing
    for thisComponent in stroopComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    return response


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
