

# has participant exert max force 3 times 
# 03/20/17
#claudia benincasa with a lot of james help
def maxGrip(d, win):

    from psychopy import visual, core
    import time
    import u3
    
    # set up window
    win = visual.Window(size=(1280, 800), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
        monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
        blendMode='avg', useFBO=True,
        )
    
    # CHECK
    #print d.configU3()
    
    time.sleep(2)
    #number of trials
    trials = 3
    
    # ----- Stimulus Presentation -----
    
    try:
        d.streamStart()
        print "steamStart"  #CHECK
        maxTrialVoltages = []
        result = []
        for x in range(trials):
            win.flip()
            time.sleep(3)
            print "x = ", x  # CHECK
            datacount = 0
            repetitions = 0
        #    # draw a threshold line for minimum grip force
        #        threshold = visual.ShapeStim(win=win, units=None, lineWidth=3, lineColor=[255,0,0], lineColorSpace='rgb',
        #                fillColor=[255,0,0], fillColorSpace='rgb', vertices=((0.5, 0.4), (0.8, 0.4)), 
        #                closeShape=True, ori=0, opacity=1, depth=-1, interpolate=True)
        # present a text message
            message1 = visual.TextStim(win=win, text='Squeeze as hard as you can with both hands for 3 seconds each time the countdown appears.', pos=(0.0, 0.7), 
                        color=[1,1,1], colorSpace='rgb', opacity=1, contrast=1, ori=0)
        #set up A TIMER ON SCREEN
            name = 0
            message2 = visual.TextStim(win=win, text='%s' %name , pos=(-0.5, -0.7), 
                        color=[1,1,1], colorSpace='rgb', opacity=1, contrast=1, ori=0)
        # draw message
            message1.setAutoDraw(True)
            win.flip()
            time.sleep(1.5)
            # initialize clock
            timer = core.Clock()
            duration = 3 # in seconds
            while (timer.getTime() <= duration):
                timeNow = timer.getTime()
                print "timeNow = ", timeNow
                if timeNow < 0.9:
                    name = 3
                elif (timeNow > 0.9) and (timeNow < 1.8):
                   name = 2
                elif timeNow > 1.8:
                   name = 1
                message2.setText(name)
                message2.setAutoDraw(True)
                #message2.setAutoDraw(False)  # double check to see if this should be turned off or not 
                for r in d.streamData():
                    repetitions +=1
                #print "Repetitions = ", repetitions  ##**CHECK**
                    if r is not None:
                    #print "Inside data stream"  ##**CHECK**
                        datacount += 1
                        print "datacount = ", datacount  #CHECK
                    #print "Datacount = ", datacount  ##**CHECK**
                        if r > 0:
                            #print "r > 0"  ##**CHECK**
                            volt =  sum(r['AIN0'])/len(r['AIN0'])  #replace with wtw.inputVoltage 
                            volt = volt * 1.5
                            result.append(volt)
                            #print volt  ##**CHECK**
                            polygon = visual.ShapeStim(win=win, units=None, lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
                                fillColor=[1,1,1], fillColorSpace='rgb', vertices=((0.6, 0), (0.7, 0),(0.7, volt), (0.6, volt)), 
                                closeShape=True, ori=0, opacity=1, depth=-1, interpolate=True)
                            polygon.setAutoDraw(True)
                            win.flip()
                            polygon.setAutoDraw(False)
                        if r < 0:
                        #print "r < 0"  ##**CHECK**
                            polygon = visual.ShapeStim(win=win, units=None, lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
                                fillColor=[1,1,1], fillColorSpace='rgb', vertices=((0.6, 0), (0.7, 0),(0.7, 0), (0.6, 0)), 
                                closeShape=True, ori=0, opacity=1, depth=-1, interpolate=True)
                            polygon.setAutoDraw(True)
                            win.flip()
                            polygon.setAutoDraw(False)
                        timeNow = timer.getTime()
                        if datacount == 16:
                            print "timeNow = duration"  #CHECK
                            #d.streamStop()
                            datacount = 0  # reset datacount back to 0 for the next iteration
                            break  #exit the streaming loop, start the next trial 
        #                if datacount >= 100:   # use this as a catch to prevent datastream from running forever
        #                        win.close()
        #                        d.streamStop()
        #                        #d.getFeedback(u3.DAC8(Dac = 0, Value = 0))   #reset analog output voltage to 0
        #                        d.close()
                    else:
                        print "No Data"
                message2.setAutoDraw(False)  # double check to see if this should be turned off or not
            maxVoltage = max(result)  #find the max voltage for this trial
            print "Max voltage = ", maxVoltage
            maxTrialVoltages.append(maxVoltage)  # append to array of max voltages for each trial    
    except:
        print "Script is Not Working"
    finally:
        d.streamStop()
        d.close()
    win.close()
    print "maxTrialVoltages = ", maxTrialVoltages
    Participant_baseline= sum(maxTrialVoltages)/len(maxTrialVoltages)
    print "Participant_baseline = ", Participant_baseline
    #can use Participant_baseline for actual experiment
    return Participant_baseline
    core.quit()
