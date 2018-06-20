# standard modules
import re
import matplotlib.pyplot as plt

#custom modules are both imported and reloaded
import wtw
reload(wtw)
import wtw.drawSample
reload(wtw.drawSample)


nTrials = 50
#specify which sampling function to test
#sampleFx = wtw.drawSample.fixed10
#sampleFx = wtw.drawSample.discreteUnif16
sampleFx = wtw.drawSample.discreteLogSpace32_1p75

#run a sequence of trials
delays = [0] * nTrials # initialize
seq = '' # initialize
for tIdx in range(nTrials):
    sampleOut = sampleFx(seq)
    delays[tIdx] = sampleOut['nextDelay']
    seq = sampleOut['seq']
print(delays)

# Create plots of 'delays' to ensure the sampling is correct
#
fig, plots = plt.subplots(nrows=3, ncols=1)
p1, p2, p3 = plots.flat
# histogram
p1.hist(delays, bins = 32)
p1.set_ylim((0,20))
p1.set_title('Sample Distribution')

# cumulative distribution
p2.hist(delays, bins = 32, histtype='step', cumulative=True)
p2.set_ylim((0,60))

#dot plots
p3.plot(delays, 'k.')
p3.set_ylim((0,40))


plt.show()




