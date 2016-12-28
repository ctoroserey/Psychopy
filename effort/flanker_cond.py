def flanker_cond(flankType, corrFlank,win,length):

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
    flankText = visual.TextStim(win=win,text=flankType,name='flankText',height=0.1)

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
