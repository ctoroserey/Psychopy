#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division
from psychopy import gui, visual, core, event
import numpy as np  # whole numpy lib is available, prepend 'np.'
import time
import exp_functions
import csv

win = visual.Window(
    size=(2560, 1440), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True)


### Importing task parameters
## Stroop
stroopColor = []
stroopWord = []
leftColor = []
rightColor = []
corrStroop = []
## Flanker
flankType = []
corrFlank = []
## Dot motion
coherDots = []
direcDots = []
corrDots = []

isi = visual.TextStim(win, text='+')
# correct tally
correct = 0

### Open the conditions file to begin import
# The order of the columns in the .csv file should be:
# stroopWord,stroopColor,leftColor,rightColor,corrStroop,flankType,corrFlank,coherDots,direcDots,corrDots
condfile = open('conditions.csv','rU') # traditionally, rb should work. However, Mac inputs \r as line delimiter, so rU changes that to \n instead. See 'open' for info
reader = csv.reader(condfile,delimiter=',')
for row in reader:
    stroopWord.append(row[0])
    stroopColor.append(row[1])
    leftColor.append(row[2])
    rightColor.append(row[3])
    corrStroop.append(row[4])
    flankType.append(row[5])
    corrFlank.append(row[6])
    coherDots.append(float(row[7]))
    direcDots.append(float(row[8]))
    corrDots.append(row[9])
condfile.close()

theseKeys = event.getKeys(keyList=['space','return'])

start = visual.TextStim(win, text='Stroop \n\n' + 'Respond with the left or right keys \n\n' + 'Indicate the COLOR of the word, not the word itself \n\n'+'Press ENTER to begin',height=0.05)
start.draw()
win.flip()
event.waitKeys(keyList=['return'])

for i in range(100):
 while correct < 6:

    if 'return' in event.getKeys(keyList=['space','return']): break

    param = np.random.randint(0,8)
    response = exp_functions.stroopCondition(stroopColor[param],stroopWord[param],leftColor[param],rightColor[param],corrStroop[param],win,2)
    isi.draw()
    win.flip()
    core.wait(2)
    # Feedback
    if 2 in response:
        correct += 1
        start.setText('Correct!')
        start.draw()
        win.flip()
        core.wait(1)
    else:
        start.setText('Incorrect')
        start.draw()
        win.flip()
        core.wait(1)

# reset correct tally
correct = 0

start = visual.TextStim(win, text='Flanker \n\n' + 'Respond with the left or right keys \n\n' + 'Indicate the direction of the center arrow \n\n'+'Press ENTER to begin',height=0.05)
start.draw()
win.flip()
event.waitKeys(keyList=['return'])

#for i in range(100):
while correct < 6:

    if 'return' in event.getKeys(keyList=['space','return']): break

    param = np.random.randint(0,8)
    response = exp_functions.flankerCondition(flankType[param],corrFlank[param],win,2)
    isi.draw()
    win.flip()
    core.wait(2)
    # Feedback
    if 2 in response:
        correct += 1
        start.setText('Correct!')
        start.draw()
        win.flip()
        core.wait(1)
    else:
        start.setText('Incorrect')
        start.draw()
        win.flip()
        core.wait(1)

 # reset correct tally
correct = 0


start = visual.TextStim(win, text='Dots \n\n' + 'Respond with the left or right keys \n\n' + 'Indicate the horizontal direction of the dots \n\n'+'Press ENTER to begin',height=0.05)
start.draw()
win.flip()
event.waitKeys(keyList=['return'])

#for i in range(100):
while correct < 6:

    if 'return' in event.getKeys(keyList=['space','return']): break

    param = np.random.randint(0,8)
    response = exp_functions.dotsCondition(coherDots[param],direcDots[param],corrDots[param],win,2)
    isi.draw()
    win.flip()
    core.wait(1)
    # Feedback
    if 2 in response:
        correct += 1
        start.setText('Correct!')
        start.draw()
        win.flip()
        core.wait(1)
    else:
        start.setText('Incorrect')
        start.draw()
        win.flip()
        core.wait(1)

start.setText('Good job!')
start.draw()
win.flip()
event.waitKeys(keyList=['return'])
