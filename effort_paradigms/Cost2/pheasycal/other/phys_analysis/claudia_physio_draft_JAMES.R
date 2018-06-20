#find the baseline (noise) for this trial so we know what is considered a squeeze
grip_analysis<- function()
{
  first_few_grip_output <- abs(grip_output[1:60]) #this is the first output for 30 ms [this value is arbitrary, we wanna get some noise]
  resting_grip_output <- mean(first_few_grip_output) #take the mean of these first 30 ms to get a baseline
  sdev_resting_output <- sd(first_few_grip_output) # gives us some measure of noise
  activity <- grip_output > resting_grip_output #anything above this baseline activity is activity although it may not be considered a grip
  max_output_of_participant <- max(grip_output)
  indices_of_max <- max_output_of_participant==grip_output
  time_max_output_of_participant <- time[indices_of_max]
  grips <- NULL 
  for (i in 1:length(activity)) {
    if (activity[i] == TRUE & grip_output[i] > threshold) {  #if the grip_output[i] > resting_out AND > threshold
      grips[i] <- grip_output[i]
    }
    else {
      grips[i] <- 0
    }
    ####
    # --- DETECT START OF GRIP ACTION ---
    time_of_starting_grip <- NULL
    indices_of_start_grip <- NULL
    # select data point to test as start of grip action
    # check to see if subset of preceeding values are NA
    # start at 500th time point - corresponds with 0.25 seconds into the experiment
    tail_of_grips <- length(grips) - 3  # use this as the end point since d = i+3 (see below) and therefore be out-of-bounds for the last 3 indices of grips
    marker <- 1
    for (i in 500:tail_of_grips) { #starts at 500 so that it may look to the values on left and right
      a <- i-499 # initial start of preceeding subset of 499 time points (relative to time point i)
      b <- i-1 # initial end of preceeding 499 time points (relative to time point i)
      c <- i+1 # initial start of subsequent 3 time points (relative to time point i)
      d <- i+3 # initial end of subsequent 3 time points (relative to time point i)
      
      preceeding_grips <- grips[a:b] == 0  # if preceeding values are below grip action threshold 
      subsequent_grips <-  grips[i] > 0 # if the subsequent values are within the standard deviation of the resting_output (i.e. noise)
      # boolean matrices - TRUE if preceeding time points are 0 (below threshold) AND subsequent time points are >0 (above threshold)
      sum_preceeding_grips <- sum(preceeding_grips)
      sum_subsequent_grips <- sum(subsequent_grips)
      # total number of TRUE's in sum_''_grips (max = 499 for sum_preceeding_grips; max = 3 for sum_subsequent_grips)
      if (sum_preceeding_grips == 499 & sum_subsequent_grips >=1 ) { # if all the preceeding indices were below threshold and the subsequent grips were above threshold
        time_of_starting_grip[marker] <- time[i]
        indices_of_start_grip[marker] <- i  # keep track of the index where the grip occurs
        marker <- marker+1
      }
    }
    
    number_of_grips <- length(time_of_starting_grip) #should be 14 for data test
  }
  # --- DETECT END OF GRIP ACTION ---
  time_of_releasing_grip <- NULL
  indices_of_releasing_grip <- NULL
  # select data point to test as start of grip release
  # check to see if subset of preceeding values are NOT NA
  # start at 500th time point - corresponds with 0.25 seconds into the experiment
  tail_of_grips2 <- length(grips) - 500  # use this as the end point since d = i+499 (see below) and therefore be out-of-bounds for the last 500 indices of grips
  marker2 <- 1
  for (i in 500:tail_of_grips2) { #starts at 500 so that it may look to the values on left and right
    a <- i-3 # initial start of preceeding subset of 3 time points (relative to time point i)
    b <- i-1 # initial end of preceeding 3 time points (relative to time point i)
    c <- i+1 # initial start of subsequent 499 time points (relative to time point i)
    d <- i+499 # initial end of subsequent 499 time points (relative to time point i)
    
    preceeding_release <- grips[i] > 0  # if the subsequent values are within the standard deviation of the resting output (i.e. noise)
    subsequent_release <- grips[c:d] == 0 # if subsequent values are below grip action threshold
    # boolean matrices - TRUE if preceeding time points are > 0 (above threshold) AND subsequent time points are 0 (below or at threshold)
    sum_preceeding_release <- sum(preceeding_release)
    sum_subsequent_release <- sum(subsequent_release)
    # total number of TRUE's in 'sum_''_grips (max = 499 TRUE)
    #we want sum_preceeding_release to always be FALSE because before a release, all the values should be larger than threshold bc u cant release unless you are gripping
    if (sum_preceeding_release >= 1  & sum_subsequent_release == 499 ) { # denotes beginning of grip - 90% of subsequent_grips == TRUE
      #starting_grip[i] <- grip_output[i]
      time_of_releasing_grip[marker2] <- time[i]
      indices_of_releasing_grip[marker2] <- i
      marker2 <- marker2+1
    }
  }
  
  number_of_releases <- length(time_of_releasing_grip) #should be 14 for data test
  
  # --- DURATION OF GRIP ACTION ---
  #time elapsed between grip and release
  duration_of_grips=NULL
  max_number_of_subtractions <- length(time_of_releasing_grip) #this length is always either the same or smaller than number of grips
  # if there are 14 grips and 13 releases, it returns 13 differences
  # if there are 13 grips and 13 releases, it also returns 13 differences
  for (i in 1:max_number_of_subtractions) {
    duration_of_grips[i] <- time_of_releasing_grip[i]-time_of_starting_grip[i] 
  }
  
  # --- MAXIMUM OUTPUT PER GRIP ACTION ---
  #finds the maximum outputs per grip
  each_maximum_grip_output <- NULL
  time_of_max_grips=NULL #output seems more relevant but might as well include
  for (i in 1: max_number_of_subtractions) {
    each_maximum_grip_output[i] <- max(grips[indices_of_start_grip[i]:indices_of_releasing_grip[i]])
  }
  
  # at the suggestion of Joe, use 'match' to find the index of the maximum grip within the window
  #   bounded by the indices_of_starting_grip[i] and indices_of_releasing_grip[i]
  subset_index <- NULL
  for (j in 1:length(each_maximum_grip_output)) {
    subset_index[j] <- match(each_maximum_grip_output[j], grips[indices_of_start_grip[j]:indices_of_releasing_grip[j]])
  }
  # then take this index, and add it to indices_of_starting_grip[i] to get its index within the entire dataset
  max_grip_indices <- subset_index + indices_of_start_grip - 1
  times_of_max_grips <- time[max_grip_indices]
  
  
  #slope of reaching the maximum for grip #####doesnt seem right
  increasing_slope_per_grip <- NULL
  for (i in 1: max_number_of_subtractions) {
    increasing_slope_per_grip[i] <- ((each_maximum_grip_output[i]-grips[indices_of_start_grip[i]]) / (times_of_max_grips[i]-time_of_starting_grip[i]))
  }
  
  #slope of leaving maximum and ending the grip ######doesnt seem right
  decreasing_slope_per_grip <- NULL
  for (i in 1: max_number_of_subtractions) {
    decreasing_slope_per_grip[i] <- ((each_maximum_grip_output[i]-grips[indices_of_releasing_grip[i]]) / (times_of_max_grips[i]-time_of_releasing_grip[i]))
  }
  
  #time to get to maximum and the time it takes to end trial from maximum
  time_to_reach_max <- NULL
  time_to_end_from_max <- NULL
  for (i in 1: max_number_of_subtractions) {
    time_to_reach_max[i] <- times_of_max_grips[i] - time_of_starting_grip[i]
    time_to_end_from_max[i] <- time_of_releasing_grip[i]- times_of_max_grips[i]
  }
}

# ---------- VOLTAGE TIMER ---------
# use the data from the voltage timer channel to find:
#   - beginning of condition block
#   - end of condition block
#   - beginning of trial
#   - sell response (end of trial)

# --- BEGINNING OF BLOCK ---
#find the baseline (noise) for the voltage channel
first_few_volts <- abs(voltage_timer[1:60]) #this is the first output for 30 ms [this value is arbitrary, we wanna get some noise]
resting_voltage <- mean(first_few_volts)
sdev_resting_voltage <- sd(first_few_volts) # gives us some measure of noise

# find beginning of condition block
beginnings_of_blocks <- NULL
indices_of_beginnings_of_blocks <- NULL

tail_of_voltage <- length(voltage_timer) - 3  # use this as the end point since d = i+3 (see below) and therefore be out-of-bounds for the last 3 indices of grips
marker <- 1
for (i in 100:tail_of_voltage) { #starts at 100 so that it may look to the values on left and right
  a <- i-99 # initial start of preceeding subset of 99 time points (relative to time point i)
  b <- i-1 # initial end of preceeding 99 time points (relative to time point i)
  c <- i+1 # initial start of subsequent 3 time points (relative to time point i)
  d <- i+3 # initial end of subsequent 3 time points (relative to time point i)
  
  preceeding_volts <- voltage_timer[a:b] < 0.04  # if preceeding values are below the resting voltage 
  subsequent_volts <-  voltage_timer[i] > 0.04 # if the subsequent values are above the resting voltage
  # boolean matrices - TRUE if preceeding time points are 0 (below threshold) AND subsequent time points are >0 (above threshold)
  sum_preceeding_volts <- sum(preceeding_volts)
  sum_subsequent_volts <- sum(subsequent_volts)
  # total number of TRUE's in sum_''_grips (max = 99 for sum_preceeding_grips; max = 3 for sum_subsequent_grips)
  if (sum_preceeding_volts == 99 & sum_subsequent_volts >=1 ) { # if all the preceeding indices were below threshold and the subsequent grips were above threshold
    beginnings_of_blocks[marker] <- time[i]
    indices_of_beginnings_of_blocks[marker] <- i  # keep track of the index where the grip occurs
    marker <- marker+1
  }
}
number_of_block_starts <- length(beginnings_of_blocks) 
# --- END OF BLOCK ---
ends_of_blocks <- NULL
indices_of_ends_of_blocks <- NULL
# select data point to test as start of grip release
# check to see if subset of preceeding values are NOT 0
# start at 100th time point 
tail_of_voltage <- length(voltage_timer) - 100  # use this as the end point since d = i+99 (see below) and therefore be out-of-bounds for the last 500 indices of grips
marker <- 1
for (i in 100:tail_of_voltage) { #starts at 100 so that it may look to the values on left and right
  a <- i-3 # initial start of preceeding subset of 3 time points (relative to time point i)
  b <- i-1 # initial end of preceeding 3 time points (relative to time point i)
  c <- i+1 # initial start of subsequent 99 time points (relative to time point i)
  d <- i+99 # initial end of subsequent 99 time points (relative to time point i)
  
  preceeding_volts <- voltage_timer[i] > 1  # if the preceeding values are > 1 (the assigned voltage for blocks)
  subsequent_volts <- voltage_timer[c:d] < 1 # if subsequent values are < 1
  # boolean matrices - TRUE if preceeding time points are > 0 (above threshold) AND subsequent time points are 0 (below or at threshold)
  sum_preceeding_volts <- sum(preceeding_volts)
  sum_subsequent_volts <- sum(subsequent_volts)
  # total number of TRUE's in 'sum_''_grips (max = 99 TRUE)
  #we want sum_preceeding_release to always be FALSE because before a release, all the values should be larger than threshold bc u cant release unless you are gripping
  if (sum_preceeding_volts >= 1  & sum_subsequent_volts == 99 ) { # denotes beginning of grip - 90% of subsequent_grips == TRUE
    ends_of_blocks[marker] <- time[i]
    indices_of_ends_of_blocks[marker] <- i
    marker <- marker+1
  }
}

number_of_block_ends <- length(ends_of_blocks) #should be 14 for data test

# --- BEGINNING OF TRIAL ---
beginnings_of_trials <- NULL
indices_of_beginnings_of_trials <- NULL

tail_of_voltage <- length(voltage_timer) - 3  # use this as the end point since d = i+3 (see below) and therefore be out-of-bounds for the last 3 indices of grips
marker <- 1
for (i in 100:tail_of_voltage) { #starts at 100 so that it may look to the values on left and right
  a <- i-99 # initial start of preceeding subset of 99 time points (relative to time point i)
  b <- i-1 # initial end of preceeding 99 time points (relative to time point i)
  c <- i+1 # initial start of subsequent 3 time points (relative to time point i)
  d <- i+3 # initial end of subsequent 3 time points (relative to time point i)
  
  preceeding_volts <- voltage_timer[a:b] < 3  # if preceeding values are below the trial voltage 
  subsequent_volts <-  voltage_timer[i] > 3 # if the subsequent values are above the trial voltage
  # boolean matrices - TRUE if preceeding time points are 0 (below threshold) AND subsequent time points are >0 (above threshold)
  sum_preceeding_volts <- sum(preceeding_volts)
  sum_subsequent_volts <- sum(subsequent_volts)
  # total number of TRUE's in sum_''_grips (max = 99 for sum_preceeding_grips; max = 3 for sum_subsequent_grips)
  if (sum_preceeding_volts == 99 & sum_subsequent_volts >=1 ) { # if all the preceeding indices were below threshold and the subsequent grips were above threshold
    beginnings_of_trials[marker] <- time[i]
    indices_of_beginnings_of_trials[marker] <- i  # keep track of the index where the grip occurs
    marker <- marker+1
  }
}
number_of_trial_starts <- length(beginnings_of_trials) 
# --- ENDS OF TRIALS ---
ends_of_trials <- NULL
indices_of_ends_of_trials <- NULL
# select data point to test as start of grip release
# check to see if subset of preceeding values are NOT 0
# start at 100th time point 
tail_of_voltage <- length(voltage_timer) - 100  # use this as the end point since d = i+99 (see below) and therefore be out-of-bounds for the last 500 indices of grips
marker <- 1
for (i in 100:tail_of_voltage) { #starts at 100 so that it may look to the values on left and right
  a <- i-3 # initial start of preceeding subset of 3 time points (relative to time point i)
  b <- i-1 # initial end of preceeding 3 time points (relative to time point i)
  c <- i+1 # initial start of subsequent 99 time points (relative to time point i)
  d <- i+99 # initial end of subsequent 99 time points (relative to time point i)
  
  preceeding_volts <- voltage_timer[i] > 3  # if the preceeding values are > 1 (the assigned voltage for blocks)
  subsequent_volts <- voltage_timer[c:d] < 3 # if subsequent values are < 1
  # boolean matrices - TRUE if preceeding time points are > 0 (above threshold) AND subsequent time points are 0 (below or at threshold)
  sum_preceeding_volts <- sum(preceeding_volts)
  sum_subsequent_volts <- sum(subsequent_volts)
  # total number of TRUE's in 'sum_''_grips (max = 99 TRUE)
  #we want sum_preceeding_release to always be FALSE because before a release, all the values should be larger than threshold bc u cant release unless you are gripping
  if (sum_preceeding_volts >= 1  & sum_subsequent_volts == 99 ) { # denotes beginning of grip - 90% of subsequent_grips == TRUE
    ends_of_trials[marker] <- time[i]
    indices_of_ends_of_trials[marker] <- i
    marker <- marker+1
  }
}

number_of_trial_ends <- length(ends_of_trials) 


#establishes anything that is above baseline as response but nessecarily a grip BUT ALSO INCLUDES GRIP

#Potentially include explicitly values above resting and below grip??? 
#===========================================================================
#max output of THIS participant and when it occurs

#set threshold which denotes a grip and intialize variables
threshold <- resting_grip_output + (25*abs(resting_grip_output)) 

#-------------------
# edit by James 5/5/17 
# uses full grip dataset (grip_output), to create a new vector where outputs not considered "grips" for our purposes are assigned values of 0
# reminder: activity <- grip_output > resting_output

 