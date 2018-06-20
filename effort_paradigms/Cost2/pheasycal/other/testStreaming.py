# file to develop/test a solution for LIFO streaming using threading.

import threading
import Queue
import u3
import time
import wtw.handgrip
import numpy as np
from psychopy import visual, core, event

hgQueue = Queue.LifoQueue()
readStream = threading.Event()
readStream.set()

# tell the U3 to start streaming
d = wtw.handgrip.openLabJack(u3) # may remove this argument?
d.streamStart()
streamObj = d.streamData()

# open a window
win = visual.Window(size=(1280, 800), fullscr=True, screen=0, allowGUI=False,
    allowStencil=False, monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, units='height')

# create a text display objects
message = visual.TextStim(win=win, ori=0, name='message', text='', font=u'Arial',
    pos=[0, 0], height=0.05, wrapWidth=None, color=u'white', colorSpace='rgb',
    alignHoriz='center')
message.setAutoDraw(True)

# set up the worker thread
t = threading.Thread(target=wtw.handgrip.streamReader,args=(readStream,streamObj,hgQueue))
t.start()

# set up clock
c = core.Clock()
priorTime = c.getTime()

# main loop
exitNow = False
while not exitNow:
    # collect DAQ data value
    hgValue = hgQueue.get()
    # display the data value
    message.setText('{:.3f}'.format(hgValue))
    win.flip()
    # check timing
    currentTime = c.getTime()
    print currentTime - priorTime
    priorTime = currentTime
    # check for a keypress respone to quit
    keysNow = event.getKeys()
    if len(keysNow) > 0:
        exitNow = True

# close down the U3
readStream.clear() # close the thread
t.join()
d.streamStop()
d.close()

# close psychopy window
win.close()
# core.quit()
