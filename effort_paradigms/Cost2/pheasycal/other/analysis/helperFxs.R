
# analysis helper functions


# split a subject's data into blocks
splitBlocks <- function(subjectData) {
  # input is a data frame with 1 subject's complete data
  # return a list of data frames, each containing the trials from one block
  # omit practice trials, which all have a TrialNumber of 1
    # (there may be practice trials before later blocks, not just the first)
  blockedData <- list()
  thisBlock <- 1
  # loop over as many blocks as exist in the data set
  while (any(subjectData$BlockNumber==thisBlock)) {
    bkIdxFirst <- max(which(subjectData$BlockNumber==thisBlock & subjectData$TrialNumber==1))
      # the last "trial 1" in this block is the first real trial.
    bkIdxLast <- max(which(subjectData$BlockNumber==thisBlock))
    blockedData[[thisBlock]] <- subjectData[bkIdxFirst:bkIdxLast, ]
    thisBlock = thisBlock + 1
  }
  return(blockedData)
}


# check the distribution of scheduled delays
scheduledDelays <- function(blockData,blockLabel) {
  cat(sprintf('Scheduled delays for %s\n',blockLabel))
  bkDelays = blockData$ScheduledDelay
  print(summary(bkDelays))
  # empirical cumulative distribution of scheduled delays
  fn <- ecdf(bkDelays)
  plot(fn, main = sprintf('Scheduled delays: %s',blockLabel))
  # autocorrelation function
  acfOutput <- acf(bkDelays, lag.max=20, main = sprintf('Scheduled delays: %s',blockLabel))
}


# plot trialwise responses in detail
trialPlots <- function(blockData,blockLabel) {
  # vectors to be plotted
  rwdIdx = blockData$TrialEarnings > 0
  quitIdx = blockData$TrialEarnings == 0
  rwdTrialNo = blockData$TrialNumber[rwdIdx]
  quitTrialNo = blockData$TrialNumber[quitIdx]
  rwdSchedDelay = blockData$ScheduledDelay[rwdIdx]
  quitSchedDelay = blockData$ScheduledDelay[quitIdx]
  rt = blockData$ResponseClockTime - blockData$TokenOnsetTime
  quitTime = rt[quitIdx]
  # other parameters
  nTrials = max(blockData$TrialNumber)
  maxDelay = max(blockData$ScheduledDelay)
  # make the plot and add series
  plot(1, type='n', xlim=c(1,nTrials), ylim=c(0,maxDelay), bty='n',
       xlab='Trial', ylab='Delay (s)', main=sprintf('Trial data: %s',blockLabel))
  lines(rwdTrialNo, rwdSchedDelay, col='blue', type='o', lwd=2, pch=16)
  lines(quitTrialNo, quitTime, col='red', type='o', lwd=2, pch=16)
  lines(quitTrialNo, quitSchedDelay, col='black', type='o', lwd=2, lty=0, pch=16)
}


# calculate kaplan-meier and area under the curve
kmsc <- function(blockData,tMax,blockLabel) {
  library(survival)
  trialDuration = blockData$ResponseClockTime - blockData$TokenOnsetTime
  isQuit = blockData$TrialEarnings == 0
  # for rewarded trials, base the duration on the reward delivery time (not the subsequent response)
  trialDuration[!isQuit] <- as.numeric(blockData$RewardOnsetTime[!isQuit]) - blockData$TokenOnsetTime[!isQuit]
  # fit the survival function
  kmfit <- survfit(Surv(trialDuration, isQuit, type='right') ~ 1, 
                 type='kaplan-meier', conf.type='none', start.time=0, se.fit=FALSE)
  # extract elements of the survival curve object (?survfit.object)
  kmT = kmfit$time
  kmF = kmfit$surv
  # add a point at zero
  kmT = c(0, kmT)
  kmF = c(1, kmF)
  # keep only points up through tMax
  keepIdx = kmT<=tMax
  kmT <- kmT[keepIdx]
  kmF <- kmF[keepIdx]
  # extend the last value to exactly tMax
  kmT <- c(kmT, tMax)
  kmF <- c(kmF, tail(kmF,1))
  # calculate auc
  auc <- sum(diff(kmT) * head(kmF,-1))
  # plot
  plot(kmT, kmF, type='s', frame.plot=FALSE, xlab='Delay (s)', ylab='Survival rate',
       main=sprintf('KMSC: %s',blockLabel), ylim=c(0,1), xlim=c(0,tMax))
  return(list(kmT,kmF,auc))
}


rewardRT <- function(blockData,blockLabel) {
  # identify rewarded trials, get delay and RT
  rwdIdx = blockData$TrialEarnings > 0
  rwdRT = blockData$ResponseClockTime[rwdIdx] - as.numeric(blockData$RewardOnsetTime[rwdIdx])
  rwdScheduledDelay = blockData$ScheduledDelay[rwdIdx]
  # plot or summarize RTs overall (including # outliers)
  
  # test & plot RT as a function of preceding delay
  corResult <- cor.test(rwdScheduledDelay, rwdRT, method='spearman')
  rhoValue = corResult$estimate
  plot(rwdScheduledDelay, rwdRT, type='p', frame.plot=FALSE, 
       xlab='Delay (s)', ylab='Reward RT (s)', ylim=c(0,1),
       main=sprintf('%s: rho = %1.2f',blockLabel,rhoValue))
}


