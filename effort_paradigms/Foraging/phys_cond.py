def phys_cond(win,length):

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

    # Stimulus setup
    physText = visual.TextStim(win=win,text='physType',name='physText',height=0.12)

    # ------Prepare to start Routine "phys"-------
    physClock = core.Clock()
    physClock.reset()  # clock, to be used in the future
    continueRoutine = True
    response = 0
    miss = 0
    corrPhys = ['left','right']
    physType = ['<','>']

    # -------Start Routine "phys"-------
    # present stimuli
    while continueRoutine and length > 0:
        physText.setText(physType[0])
        physText.draw()
        win.flip()
        core.wait(0.5)
        theseKeys = event.getKeys(keyList=['left', 'right','space','escape'])
        if len(theseKeys) == 0:
            #print 'miss'
            miss += 1
        elif len(theseKeys) > 0:
            if 'escape' in theseKeys:
                core.quit()
            elif 'space' in theseKeys:
                response = 1
                continueRoutine = False
            elif (theseKeys[-1] == str(corrPhys[0])) or (theseKeys[-1] == corrPhys[0]):
                #print 'correct!'
                response = 2
            else:
                #print 'incorrect'
                miss += 1

        if miss > 3:
            response = 3
            continueRoutine = False

        physText.setText(physType[1])
        physText.draw()
        win.flip()
        core.wait(0.5)
        theseKeys = event.getKeys(keyList=['left', 'right','space','escape'])
        if len(theseKeys) == 0:
            #print 'miss'
            miss += 1
        elif len(theseKeys) > 0:
            if 'escape' in theseKeys:
                core.quit()
            elif 'space' in theseKeys:
                response = 1
                continueRoutine = False
            elif (theseKeys[-1] == str(corrPhys[1])) or (theseKeys[-1] == corrPhys[1]):
                #print 'correct!'
                response = 2
            else:
                #print 'incorrect'
                miss += 1

        if miss > 3:
            response = 3
            continueRoutine = False

        length -= 1

    return response
