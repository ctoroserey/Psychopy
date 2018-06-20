
# single subject analysis 
# - OK select a file interactively
# - check frame times
# - OK plot the distribution of scheduled delays (check the sequence?)
# - OK standard single-subject trial plot
# - OK survival curve and AUC for each block
# - reward RTs, overall and as a function of preceding delay


# source analysis sub-functions
source('helperFxs.R')

# prompt to select a file
library(tcltk)
fname = tk_choose.files(default = "../data/*", caption = "Select a data file.", multi = FALSE, 
                        filter = matrix(c("Text", 'wtwTask8*.csv'), 1, 2, byrow = TRUE))
print(fname)

# load the file
subjectData = read.csv(fname, as.is = TRUE)

# interpret the counterbalance condition
id <- unique(subjectData$X1..Participant)
cbal <- unique(subjectData$X2..Counterbalance)
if (cbal==0 | cbal==1) {timingCond = c('HP', 'HP')} else {timingCond = c('LP', 'LP')} # timing condition
if (cbal==0 | cbal==2) {effortCond = c('Waiting', 'Working')} else {effortCond = c('Working', 'Waiting')} # effort condition
cat(sprintf('=====\nParticipant %d, cbal = %d\n=====\n',id,cbal))

# split by block, removing practice rows, if any
blockedData <- splitBlocks(subjectData)
nBlocks = length(blockedData)
blockLabels = vector()
for (bkIdx in 1:nBlocks) {
  blockLabels[bkIdx] = sprintf('#%d, Block %d, %s %s',id,bkIdx,timingCond[bkIdx],effortCond[bkIdx])
}

# plot the distribution of scheduled delays in each block
for (bkIdx in 1:nBlocks) {
  scheduledDelays(blockedData[[bkIdx]],blockLabels[bkIdx])
}

# make single-subject trial plots
for (bkIdx in 1:nBlocks) {
  trialPlots(blockedData[[bkIdx]],blockLabels[bkIdx])
}

# kaplan-meier survival curve
tMax = 16 # survival curve upper bound
for (bkIdx in 1:nBlocks) {
  km <- kmsc(blockedData[[bkIdx]],tMax,blockLabels[bkIdx])
  cat(sprintf('Block %d AUC: %1.2f of %1.2f s\n',bkIdx,km[[3]],tMax))
}

# rt, overall and as a function of preceding latency
# [tmp note: good illustration is 205]
for (bkIdx in 1:nBlocks) {
  rewardRT(blockedData[[bkIdx]],blockLabels[bkIdx])
}








