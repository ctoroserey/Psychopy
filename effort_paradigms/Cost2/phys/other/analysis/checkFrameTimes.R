
# prompt to select a file
library(tcltk)
fname = tk_choose.files(default = "../data/*", caption = "Select a frame timing file.", multi = FALSE, 
                        filter = matrix(c("Text", '*frameTimes*.txt'), 1, 2, byrow = TRUE))
print(fname)

# load the frame time data
frameTimeData  <- scan(fname,sep=",")
frameDuration <- diff(frameTimeData)
refreshCount = frameDuration*60

# plot the cumulative distribution
x = ecdf(refreshCount)
print(summary(x))
plot(x)

# report on how many intervals exceeded 1 screen refresh
missIdx = round(refreshCount)>1
nMiss = sum(missIdx)
missTime = frameTimeData[missIdx]
print(missTime)
plot(missIdx) # plot when the misses occurred

