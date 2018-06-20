
# runs tests of subfunctions in wtw

# standard modules
import re
import matplotlib.pyplot as plt

# custom modules are both imported and reloaded
import wtw
reload(wtw)
import wtw.drawSample
reload(wtw.drawSample)


######################
def test_drawSample():
    ## parameters
    nTrials = 100
    ## specify which sampling function to test
    # sampleFx = wtw.drawSample.fixed10
    sampleFx = wtw.drawSample.discreteUnif16
    # sampleFx = wtw.drawSample.discreteLogSpace32_1p75
    
    # run a sequence of trials
    delays = [0] * nTrials # initialize
    seq = '' # initialize
    for tIdx in range(nTrials):
        sampleOut = sampleFx(seq)
        delays[tIdx] = sampleOut['nextDelay']
        seq = sampleOut['seq']
    print(delays)
    
    # Create plots of 'delays' to ensure the sampling is correct
    fig, plots = plt.subplots(nrows=3, ncols=1)
    p1, p2, p3 = plots.flat
    # histogram
    p1.hist(delays, bins = 32)
    p1.set_ylim((0,nTrials))
    p1.set_title('Sample Distribution')
    # cumulative distribution
    p2.hist(delays, bins=100, histtype='step', cumulative=True)
    p2.set_ylim((0,nTrials+10))
    #dot plots
    p3.plot(delays, 'k.')
    p3.set_ylim((0,40))

    plt.show()


########################
def test_nextQuantile():
    nTrials = 20
    nQuantiles = 8
    seq = ''
    trialQuantile = []
    for trialIdx in range(nTrials):
        quantileOutput = wtw.drawSample.nextQuantile(nQuantiles, seq)
        seq = quantileOutput['seq']
        trialQuantile.append(quantileOutput['nextQuantile'])
    print trialQuantile
    print seq
    # print item frequences
    print 'Item frequences:'
    for i in range(nQuantiles):
        freq = seq.count(str(i))
        print '  ' + str(i) + ': ' + str(freq)
    # print transition frequences
    print 'Transition frequencies:'
    for i in range(nQuantiles):
        for j in range(nQuantiles):
            # freq = seq.count(str(i) + str(j)) # only counts non-overlapping sequences
            freq = len(re.findall('(?=({}{}))'.format(i,j), seq))
            print '  ' + str(i) + str(j) + ': ' + str(freq)
        


