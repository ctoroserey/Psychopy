# wtw.handgrip
# submodule with functions for interfacing with
# the Biopac dynamometer via the LabJack DAQ

from psychopy import visual, core, event
import time
import numpy as np
try: import u3
except: pass

#######################################
# attempt to connect to the LabJack DAQ
def openLabJack(u3):
    # Check if stimulus computer can open LabJack U3
    # James Lynch
    # 2/28/17
    d = 0
    try:
        d = u3.U3()
        d.configU3()
        d.configIO(FIOAnalog = 1)
        d.configAnalog(u3.FIO7)
        d.streamConfig( NumChannels = 1, SamplesPerPacket = 25, PChannels = [ 7 ], NChannels = [ 31 ], Resolution = 3, SampleFrequency = 1600)
        d.packetsPerRequest = 1
        # d.streamConfig( NumChannels = 1, PChannels = [ 7 ], ScanFrequency = 1000)
    except:
        print "LabJack U3 not connected"
        pass
    return d


################################################
# mouse position; use in case DAQ is unavailable
def inputMouse():
    mouse = event.Mouse()
    pos = mouse.getPos()
    yPos = pos[1]
    return yPos


##############################################
# read the handgrip input voltage from the DAQ
def hgInput(LabJack):
    # Function to get voltage value from LabJack data stream
    #    voltage value comes from hand dyamometer (BioPack/Acqknowledge)
    # Returns voltage value to script that called this function
    #
    # James Lynch
    # 3/3/17

    if LabJack == 0:
        # DAQ is unavailable; use mouse position instead
        position = inputMouse()
        return position

    dataCount = 0
    r = LabJack.streamData()
    sampleNow = r.next()
    sampleValues = sampleNow['AIN7']
    volt = np.mean(sampleValues)
    # usableSamples = sampleValues[200:800] # for 50k Hz
    # volt = np.median(usableSamples)

    # for r in LabJack.streamData():
    #     if r is not None:
    #         dataCount += 1  #each dataCount = 1 'request' to read the input of the LabJack buffer
            #print "Data count = ", dataCount  #CHECK
            #packetCount += r['numPackets']
            # if r > 0:
                #  'sample' - one reading from the LabJack channel
                # samples = len(r['AIN7'])  # number of samples per "request" - per iteration of d.streamData()
                #print "Number of samples = ", samples   #**CHECK**

                # --- Forumula taken from streamTest.py in '~/Desktop/LabJackPython-5-26-15/Examples ---
                #              r has too many data points to graph as is - 1200 samples per request
                #                 - frameRate isn't fast enough to plot this input --> input = ~19354Hz when dataCount limit = 150
                #              instead, set volt = average voltage per request
                #                 - input = ~16Hz when dataCount limit = 150

                # volt =  sum(r['AIN7'])/len(r['AIN7'])

                #print "Original voltage = ", volt  #**CHECK**

                # volt = volt*1.5  # 1.5 is an arbitrary value for viewing purposes only - window height ranges from (-1, 1)
                #print "Scaled voltage = ", volt
                #respArgs['volt'] = volt
                #print 'respArgs[volt] = ', volt  #CHECK
            # if dataCount >= 1:
                # 16.128 requests per second
                # Assess voltage every request, then go through the rest of the while loop, before starting again
                # If no dataCount limit is set, experiment gets stuck in the for loop indefinitely
                #   - doesn't reach any of the subsequent code
                # respArgs['volt'] = volt
                # break
    return volt

#########################################
# monitor streaming input using threading
# this is a worker (target) function
def streamReader(readStream,streamObj,hgQueue):
    # readStream is a threading.Event object
    # streamObj is a U3.streamData object
    # hgQueue is a Queue.LifoQueue object
    while readStream.isSet():
        if not streamObj:
            hgQueue.put(inputMouse()) # use the mouse instead
            time.sleep(0.016) # approximately match the frequency
        else: # if the LabJack U3 is available
            thisSample = streamObj.next() # wait for the next 25-sample packet
            if thisSample is not None:
                thisData = thisSample['AIN7']
                hgQueue.put(np.mean(thisData)) # return the mean
        # might add code here to empty the queue

#########################################################
# collect a reading from AIN7 using command-response mode
# averages a specified number of samples.
def hgInputCR(LabJack=0,nSamples=4):

    # if the DAQ is unavailable, use mouse position instead
    if LabJack == 0:
        position = inputMouse()
        return position

    # average the requested number of samples
    volt = []
    for i in range(nSamples):
        # volt = LabJack.getFeedback(u3.AIN(PositiveChannel = 0, LongSettling=False, QuickSample=False)
        volt.append(LabJack.getAIN(7, 31, False, False)) # negative channel 31 means single-ended
        # volt.append(LabJack.getFeedback(u3.AIN(7, 31, False, False)))
    return np.mean(volt)

#####################################
# write a pulse to the marker channel
def markerPulse(volts):
    # voltageToDACBits(self, volts, dacNumber = 0, is16Bits = False)
    pass




#####################################################
# series of functions to set the event marker channel
# outputs a voltage signal via LabJack to BioPac/Acqknowledge
# James Lynch
# 3/3/17
def startBlockSignal(d):
    # step voltage up to 1 volt, signaling beginning of time block
    # Stays at 1 volt for duration of block
    try:
        d.getFeedback(u3.DAC8(Dac = 0, Value = 49))
    except:
        print "LabJack not connected"
        pass
def trialOnsetSignal(d):
    # signal onset of individual trials
    # Brief step up to 2 volts
    try:
        d.getFeedback(u3.DAC8(Dac = 0, Value = 149))
        #d.getFeedback(u3.DAC8(Dac = 0, Value = 49))
    except:
        print "LabJack not connected"
        pass
def trialEndSignal(d):
    # end trialOnsetSignal
    try:
        d.getFeedback(u3.DAC8(Dac = 0, Value = 49))
    except:
        print "LabJack not connected"
        pass
def stopBlockSignal(d):
    # step voltage down, signaling end of time block
    try:
        d.getFeedback(u3.DAC8(Dac = 0, Value = 0))
    except:
        print "LabJack not connected"
        pass


####################################################
# minimalistic task to display DAQ input numerically
def testInput():
    useStreaming = True
    # open the DAQ if available
    try:
        LabJack = openLabJack(u3)
        if useStreaming:
            LabJack.streamStart()
    except:
        LabJack = 0 # can run using the mouse
    # open a window
    win = visual.Window(size=(1280, 800), fullscr=True, screen=0, allowGUI=False,
        allowStencil=False, monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
        blendMode='avg', useFBO=True, units='height')
    # create a text display objects
    message = visual.TextStim(win=win, ori=0, name='message', text='', font=u'Arial',
        pos=[0, 0], height=0.05, wrapWidth=None, color=u'white', colorSpace='rgb',
        alignHoriz='center')
    message.setAutoDraw(True)
    # main loop
    exitNow = False
    while not exitNow:
        # collect DAQ data value
        # d = hgInputCR(LabJack)
        if useStreaming:
            d = hgInput(LabJack)
        else:
            d = hgInputCR(LabJack)
        # display the data value
        message.setText('{:.3f}'.format(d))
        win.flip()
        # check for a keypress respone to quit
        keysNow = event.getKeys()
        if len(keysNow) > 0:
            exitNow = True
    # when done
    try:
        if useStreaming:
            LabJack.streamStop()
            LabJack.close()
    except:
        pass
    win.close()
    core.quit()


###########################################################
# minimalistic function to test the time taken for sampling
# nb: this won't run in mouse mode, no window is opened.
def testInputTiming():
    # set number of samples
    nSamples = 100
    # determine whether to use streaming or command/response mode
    # be sure to uncomment streamConfig line in openLabJack
    useStreaming = True
    # open the DAQ if available
    LabJack = openLabJack(u3)
    if useStreaming:
        LabJack.streamStart()
    # create a psychopy clock
    clock = core.Clock()
    # messages
    if useStreaming:
        print 'Streaming mode.'
    else:
        print 'Command/response mode.'
    print 'Collecting {:d} samples...'.format(nSamples)
    # main loop
    sampleTimes = []
    for i in range(nSamples):
        # collect DAQ data value
        if useStreaming:
            d = hgInput(LabJack)
        else:
            d = hgInputCR(LabJack)
        # log current time
        sampleTimes.append(clock.getTime())
        # add a delay (to mimic other processing)
        core.wait(0.01)
    # report on the inter-sample intervals
    print 'Done.'
    if useStreaming:
        LabJack.streamStop()
    LabJack.close()
    ISIs = np.diff(sampleTimes)
    print "~ seconds/request ~"
    print('min interval = {:.6f}'.format(np.min(ISIs)))
    print('median = {:.6f}'.format(np.median(ISIs)))
    print('75th percentile = {:.6f}'.format(np.percentile(ISIs,75)))
    print('95th percentile = {:.6f}'.format(np.percentile(ISIs,95)))
    print('99th percentile = {:.6f}'.format(np.percentile(ISIs,99)))
    print('max = {:.6f}'.format(np.max(ISIs)))

    #print "%s requests" % nSamples
    #packetsPerRequest = packetCount/nSamples
    #print "%s packetsPerRequest" % packetsPerRequest
    #sampleTotal = nSamples * samplesPerRequest
    #print "%s samplesPerPacket" % LabJack.streamSamplesPerPacket
    #print "%s samplesPerRequest" % samplesPerRequest
    #print "Total # of samples = ", sampleTotal



#####################################################
# elicit the participant's max grip force, which will
# be used to calibrate the force level threshold.
# written by Claudio Benincasa, James Lynch, and Joe McGuire
def maxGrip(LabJack, win):
    # this function is called by a wrapper function below called 'calibrate'

    # open stream
    if LabJack != 0:
        # LabJack.streamStart()
        pass

    ##### create stimulus objects #####
    # instruction message
    txt0 = 'Grip force calibration. '
    txt2 = 'When the screen says "Grip now," squeeze as hard as you can with both hands. '
    txt3 = 'When it says "Relax," relax. '
    txt4 = 'Press a key when you are ready to start. '
    txtAll = txt0 + '\n\n' + txt2 + txt3 + '\n\n' + txt4
    message1 = visual.TextStim(win=win, text=txtAll, pos=(0, 0),
        color=[1,1,1], height=0.05, wrapWidth=1.2)
    # grip commands
    message2 = visual.TextStim(win=win, text='' , pos=(0, -0.1),
        color=[1,1,1], height=0.05)
    # clock object
    timer = core.Clock()
    # visible force-level meter
    meter = visual.Rect(win=win, fillColor=[0.5, 0.5, 0.5], pos=(0, 0), width=0.1, height=0,
        autoLog=False, name='gripCalibrationMeter')

    # initialize to collect voltages for both max force and rest
    eventType = ['relax', 'grip', 'relax', 'grip', 'relax', 'grip', 'relax'] # the sequence of event types
    instruc = {'grip':'GRIP NOW!', 'relax':'Relax.'} # the visible instruction for each event type
    results = {'grip':[], 'relax':[]} # initialize to store results
    duration = 2 # duration in s of each grip or relax event

    # display initial instruction
    message1.setAutoDraw(True)
    win.flip()
    core.wait(1, hogCPUperiod=0) # do not accept keypress for the first 1 s
    event.waitKeys()
    message1.setAutoDraw(False)
    win.flip()
    core.wait(1) # 1 s blank before we start

    # display calibration events
    message2.setAutoDraw(True)
    meter.setAutoDraw(True)
    for b in eventType:
        message2.setText(instruc[b])
        blockResults = []
        timer.reset()
        while timer.getTime() <= duration:
            # log current reading
            volt = hgInputCR(LabJack)
            blockResults.append(volt)

            # update meter
            meter.pos = (0, 0.5*volt)
            meter.height = volt
            win.flip()
            # check for quit (the Esc key)
            if event.getKeys(keyList=["escape"]):
                if LabJack != 0: # close the DAQ stream if applicable
                    # LabJack.streamStop()
                    LabJack.close()
                core.quit()
        # at the end of the block store a summary of the results.
        results[b].append(np.median(blockResults))

    # after all trials, clear the display and stop the stream
    message2.setAutoDraw(False)
    meter.setAutoDraw(False)
    if LabJack != 0:
        # LabJack.streamStop()
        pass

    # return results to the wrapper function, which will
    # analyze them and re-run the calibration if necessary.
    return results


#########################################################
# wrapper function for the grip-force calibration routine
# runs the routine, checks results, re-runs if necessary
def calibrate(LabJack, win):

    # create a text object in case calibration must be repeated
    msgRepeat = visual.TextStim(win=win, text='Calibration will be repeated.',
        pos=(0, 0), color=[1,1,1], height=0.05)

    ok = False
    while not ok:

        calibResults = maxGrip(LabJack, win)
        # calibResults is a dict with keys 'grip' and 'relax'
        # each indexes a list with one median force level per event

        print 'calibration results:'
        print calibResults

        # analysis
        gripMedian = np.median(calibResults['grip'])
        relaxMedian = np.median(calibResults['relax'])
        diffOfMedians = gripMedian - relaxMedian
        gripRange = np.max(calibResults['grip']) - np.min(calibResults['grip'])
        relaxRange = np.max(calibResults['relax']) - np.min(calibResults['relax'])

        # criterion for a valid reading:
        # the difference should be large relative to the variance (range)
        # within either event type.
        if diffOfMedians > 2 * np.max([gripRange, relaxRange]):
            ok = True
        else:
            # display a message saying the calibration will be repeated.
            msgRepeat.setAutoDraw(True)
            win.flip()
            core.wait(2)
            msgRepeat.setAutoDraw(False)

    # when finished, return a single value for 'grip' and 'relax'
    return {'grip':gripMedian, 'relax':relaxMedian}
