def dots_cond()
# ------Prepare to start Routine "dots"-------
t = 0
dotsClock.reset()  # clock
frameN = -1
continueRoutine = True
routineTimer.add(2.000000)
# update component parameters for each repeat
dots_2.setFieldCoherence(coherDots)
dots_2.setDir(direcDots)
dots_resp = event.BuilderKeyResponse()
Quit = event.BuilderKeyResponse()
# keep track of which components have finished
dotsComponents = [dots_2, dots_resp, Quit]
for thisComponent in dotsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "dots"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = dotsClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *dots_2* updates
    if t >= 0 and dots_2.status == NOT_STARTED:
        # keep track of start time/frame for later
        dots_2.tStart = t
        dots_2.frameNStart = frameN  # exact frame index
        dots_2.setAutoDraw(True)
    frameRemains = 0 + 2- win.monitorFramePeriod * 0.75  # most of one frame period left
    if dots_2.status == STARTED and t >= frameRemains:
        dots_2.setAutoDraw(False)

    # *dots_resp* updates
    if t >= 0.0 and dots_resp.status == NOT_STARTED:
        # keep track of start time/frame for later
        dots_resp.tStart = t
        dots_resp.frameNStart = frameN  # exact frame index
        dots_resp.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    frameRemains = 0.0 + 2.0- win.monitorFramePeriod * 0.75  # most of one frame period left
    if dots_resp.status == STARTED and t >= frameRemains:
        dots_resp.status = STOPPED
    if dots_resp.status == STARTED:
        theseKeys = event.getKeys(keyList=['left', 'right'])

        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        # was this 'correct'?
        if (dots_resp.keys == str('corrDots')) or (dots_resp.keys == 'corrDots'):
            dots_resp.corr = 1
        else:
            dots_resp.corr = 0

    # *Quit* updates
    if t >= 0.0 and Quit.status == NOT_STARTED:
        # keep track of start time/frame for later
        Quit.tStart = t
        Quit.frameNStart = frameN  # exact frame index
        Quit.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(Quit.clock.reset)  # t=0 on next screen flip
    frameRemains = 0.0 + 2.0- win.monitorFramePeriod * 0.75  # most of one frame period left
    if Quit.status == STARTED and t >= frameRemains:
        Quit.status = STOPPED
    if Quit.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])

        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            Quit.keys = theseKeys[-1]  # just the last key pressed
            Quit.rt = Quit.clock.getTime()
            # a response ends the routine
            continueRoutine = False

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in dotsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

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
# check responses
if Quit.keys in ['', [], None]:  # No response was made
    Quit.keys=None
thisExp.addData('Quit.keys',Quit.keys)
if Quit.keys != None:  # we had a response
    thisExp.addData('Quit.rt', Quit.rt)
thisExp.nextEntry()
# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
