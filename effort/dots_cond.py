def dots_cond(coherDots,direcDots,corrDots,win,length):

# To do:
#    - find out how to log the data properly, and trim further
#    - remove Quit_stroop
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
    dots = visual.DotStim(
        win=win,name='dots',nDots=100,
        dotSize=8,speed=0.003,fieldSize=1,
        fieldShape='circle',signalDots='same', noiseDots='direction',
        dotLife=1000)


    # ------Prepare to start Routine "dots"-------
    t = 0
    endExpNow = False # putative global quit, kept there because PsychoPy acts up when removed
    routineTimer = core.CountdownTimer() # to track time remaining of each (non-slip) routine
    dotsClock = core.Clock()
    dotsClock.reset()  # clock
    continueRoutine = True
    routineTimer.add(length)
    # update component parameters for each repeat
    dots.setFieldCoherence(coherDots)
    dots.setDir(direcDots)
    dots_resp = event.BuilderKeyResponse()
    Quit_dots = event.BuilderKeyResponse() # delete this and use 'dots_resp' instead.
    # keep track of which components have finished
    dotsComponents = [dots, dots_resp, Quit_dots]
    for thisComponent in dotsComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED


    response = 0
    # -------Start Routine "dots"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = dotsClock.getTime()

        # *dots* updates
        if dots.status == NOT_STARTED:
            dots.setAutoDraw(True)

        # response check
        if dots_resp.status == NOT_STARTED:
            # keep track of start time/frame for later
            dots_resp.tStart = t
            dots_resp.status = STARTED
            # keyboard checking is just starting
            event.clearEvents(eventType='keyboard')
        if dots_resp.status == STARTED:
            theseKeys = event.getKeys(keyList=['left', 'right','space'])

            # check for experiment quit:
            if "escape" in theseKeys:
                endExpNow = True
            # check for trial quit:
            if 'space' in theseKeys:
                #Quit_dots.keys = theseKeys[-1]  # just the last key pressed
                #Quit_dots.rt = Quit_dots.clock.getTime()
                continueRoutine = False
            # if not quit, then record response
            elif len(theseKeys) > 0:
                print 'but i pressed!'
                dots_resp.keys = theseKeys[-1] # just the last key pressed
                # was this correct?
                if (dots_resp.keys == str(corrDots)) or (dots_resp.keys == corrDots):
                    #(dots_resp.keys == str('corrDots')) or (dots_resp.keys == 'corrDots'):
                    print 'correct!'
                    dots_resp.corr = 1
                    response = 2
                    #elif  (dots_resp.keys is not str(corrDots)) or (dots_resp.keys is not corrDots):
                    #    dots_resp.corr = 0
                    #    response = 3
            else: # no response
                response = 3

        # a component has requested a forced-end of Routine
        if not continueRoutine:
            response = 1            # if not quit, then record response
            for thisComponent in dotsComponents:
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


    # -------Ending Routine "dots"-------
    for thisComponent in dotsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    return response

    # check responses
    #if Quit.keys in ['', [], None]:  # No response was made
    #    Quit.keys=None
    #thisExp.addData('Quit.keys',Quit.keys)
    #if Quit.keys != None:  # we had a response
    #    thisExp.addData('Quit.rt', Quit.rt)
    #thisExp.nextEntry()
    ## these shouldn't be strictly necessary (should auto-save)
    #thisExp.saveAsWideText(filename+'.csv')
    #thisExp.saveAsPickle(filename)
    #logging.flush()
    ## make sure everything is closed down
    #thisExp.abort()  # or data files will save again on exit
    #win.close()
    #core.quit()
