# wtw.detectResponse
# alternative functions for detecting a "Sell" response

from psychopy import event
from pyglet.window import key
# import u3
import wtw
# import wtw.inputVoltage
import wtw.handgrip
import threading
import Queue


###############################
# 1. press the spacebar to sell
def pressSpaceBar(respArgs):
    blockClock = respArgs['blockClock']
    responded = False
    responseClockTime = None
    keysNow = event.getKeys(keyList=['space'], timeStamped=blockClock)
    if len(keysNow) > 0:
        responded = True
        responseClockTime = keysNow[0][1]
            # return the time of the first key press
            # (each key press is stored as a tuple (key, time))
    return {'responded':responded, 'responseClockTime':responseClockTime, 'respArgs':respArgs}


###########################################################
# 2. repeatedly key-press to persist, stop pressing to sell
def stopPressingSpaceBar(respArgs):
    blockClock = respArgs['blockClock']
    responded = False
    responseClockTime = None
    return {'responded':responded, 'responseClockTime':responseClockTime, 'respArgs':respArgs}


#######################################################
# 3. hold down the spacebar to persist, release to sell
def releaseSpaceBar(respArgs):
    blockClock = respArgs['blockClock']
    keySH = respArgs['keySH']
    responded = False
    responseClockTime = None
    if not keySH[key.SPACE]:
        responded = True
        responseClockTime = blockClock.getTime() # will only be checked once per refresh
    return {'responded':responded, 'responseClockTime':responseClockTime, 'respArgs':respArgs}


#################################
# 4. squeeze the handgrip to sell
def squeezeHandGrip(respArgs):
    blockClock = respArgs['blockClock']
    threshold = respArgs['threshold']
    hgQueue = respArgs['hgQueue']
    hgValue = hgQueue.get()
    while hgQueue.qsize() > 0: # remove excess entries
        try:
            hgQueue.get(block=False)
        except:
            pass
    responded = False
    responseClockTime = None
    if hgValue > threshold:
        responded = True
        responseClockTime = blockClock.getTime() # will only be checked once per refresh
    return {'responded':responded, 'responseClockTime':responseClockTime, 'gripForce':hgValue, 'respArgs':respArgs}


#####################################################
# 5. squeeze the handgrip to persist, release to sell
def releaseHandGrip(respArgs):
    blockClock = respArgs['blockClock']
    threshold = respArgs['threshold']
    hgQueue = respArgs['hgQueue']
    hgValue = hgQueue.get()
    while hgQueue.qsize() > 0: # remove excess entries
        try:
            hgQueue.get(block=False)
        except:
            pass
    responded = False
    responseClockTime = None
    if hgValue < threshold:
        responded = True
        responseClockTime = blockClock.getTime() # will only be checked once per refresh
    return {'responded':responded, 'responseClockTime':responseClockTime, 'gripForce':hgValue, 'respArgs':respArgs}
