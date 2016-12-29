def stroop_cond(color, word, rgbOne, rgbTwo, corrStroop, win,length):

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

    # Stimuli setup
    target = visual.TextStim(win=win,text=word,name='target',color=color,colorSpace='rgb',height=0.25);
    circleLeft = visual.Polygon(win=win,units='cm',fillColor=rgbOne,fillColorSpace='rgb',edges=1000,size=(2, 2),pos=(-4, -3))
    circleRight = visual.Polygon(win=win,units='cm',fillColor=rgbTwo,fillColorSpace='rgb',edges=1000, size=(2, 2),pos=(4, -3))


    # Prepare to start Routine "stroop"
    stroopClock = core.Clock()
    stroopClock.reset()  # clock, to be used in the future
    response = 0
    RT = 0

    # -------Start Routine "stroop"-------
    # present stimuli
    circleLeft.draw()
    circleRight.draw()
    target.draw()
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
            elif (theseKeys[-1] == str(corrStroop)) or (theseKeys[-1] == corrStroop):
                #print 'correct!'
                response = 2
            else:
                #print 'incorrect'
                response = 3

## IMPORTANT: to return timestamps along with the answer, use a tuple like: 'return (response, RT)'
    return (response)
