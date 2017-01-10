def dots_cond(coherDots,direcDots,corrDots,win,length):

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
    dots = visual.DotStim(
        win=win,name='dots',coherence=coherDots,dir=direcDots,nDots=100,
        dotSize=8,speed=0.003,fieldSize=1,
        fieldShape='circle',signalDots='same', noiseDots='direction',
        dotLife=1000)


    # ------Prepare to start Routine "dots"-------
    dotsClock = core.Clock()  # clock, to be used in the future
    response = 0

    # -------Start Routine "dots"-------
    for i in range(90):
        dots.draw()
        win.flip()
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
            elif (theseKeys[-1] == str(corrDots)) or (theseKeys[-1] == corrDots):
                #print 'correct!'
                response = 2
            else:
                #print 'incorrect'
                response = 3

    return response
