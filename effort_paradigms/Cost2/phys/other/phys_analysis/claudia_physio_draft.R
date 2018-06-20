#Claudia Benincasa
# 04/11/17

path <- "/Users/cdlab-admin/Downloads" #Downloads can be replaced by wherever we store our data
setwd(path) #sets directory to appropriate place
getwd() #quick check to make sure it is in the right place

#copy hand grip data 
mydata<- read.table("data_Test.txt", fill=TRUE)

######NEED TO MAKE THIS SO WE CAN JUST LOAD ANY PARTICIPANT DATA

#takes the column representing time and takes all the values
time <- mydata[1]
number_of_entries <- as.numeric(length(mydata[[1]])) #total number of elements in first column of my data
time<- time[8:number_of_entries,] #rewrites time so the first value is 0 and the last value is the latest time measurement
time <- as.numeric(levels(time))[time] #makes time a number instead of a factor while retaining its value
                                       #instead of a stored value
number_of_observations <- number_of_entries-7 #since we start at 8 

#takes the column representing output and takes all the values
grip_output <- mydata[2]
grip_output <- grip_output[8:number_of_entries,]
grip_output <- as.numeric(levels(grip_output))[grip_output] #same process as above but uses the second column of data

#actual data 
time_and_output<-data.frame(time,grip_output)

#find the baseline for this trial so we know what is considered a squeeze
first_few_output <- grip_output[1:60] #this is the first output for 30 ms [this value is arbitrary, we wanna get some noise]
resting_output <- mean(first_few_output) #take the mean of these first 30 ms to get a baseline

#establishes anything that is above baseline as response but nessecarily a grip BUT ALSO INCLUDES GRIP
activity <- grip_output > resting_output #anything above this baseline activity is activity althought it may not be considered a grip
indicies_of_activity <- grip_output==activity #the indices of where activity is occuring so we can find the time as well as output
time_of_activity <- time[indicies_of_activity]

#Potentially include explicitly values above resting and below grip??? 
#===========================================================================
#max output of THIS participant and when it occurs
max_output_of_participant <- max(grip_output)
indicies_of_max <- max_output_of_participant==grip_output
time_max_output_of_participant <- time[indicies_of_max]

#set threshold which denotes a grip and intialize variables
threshold <- resting_output + (5*abs(resting_output)) ########totally arbitrary, can find suitable way later!!
start_of_grip<-NULL #makes place to store data
end_of_grip <- NULL
length_of_grip <- NULL
max_outputs_for_each_grip <- NULL
time_of_max_outputs_for_each_grip <- NULL
#-------------------
outputs_considered_grip <- NULL #records all values considered GRIPS
for (i in 1:number_of_observations) {
  if (grip_output[i] > threshold) { 
    outputs_considered_grip[i] <- grip_output[i]
  }  
}  

REAL_outputs_considered_grip=NULL ##is making sure we don't include random blips above threshold 
for (i in 1:number_of_entries) {
  if (is.na(outputs_considered_grip[i])==FALSE & is.na(outputs_considered_grip[i+1])==FALSE & is.na(outputs_considered_grip[i+2])==FALSE & is.na(outputs_considered_grip[i+3])==FALSE & is.na(outputs_considered_grip[i+4])==FALSE & is.na(outputs_considered_grip[i+5])==FALSE & is.na(outputs_considered_grip[i+6])==FALSE & is.na(outputs_considered_grip[i+7])==FALSE) {
    REAL_outputs_considered_grip[i] <-outputs_considered_grip[i] #####decide how many in a row we want ###needs altered a bit
  }
     else {
      REAL_outputs_considered_grip[i] <- NA
  }
}


starting_grip <- NULL
for (i in 2:number_of_observations) { #starts at 2 so that it may look to the values on left and right
  if (is.na(REAL_outputs_considered_grip[i-1])==TRUE & is.na(REAL_outputs_considered_grip[i])==FALSE & is.na(REAL_outputs_considered_grip[i+1])==FALSE) { #denotes beginning of grip
    starting_grip[i] <- grip_output[i]
  }
  else {
    starting_grip[i] <- NA
  }  
}
indicies_of_starting_grip <- starting_grip== grip_output 
time_of_starting_grip <- time[indicies_of_starting_grip] #gives us the time where the grip started for each peack
time_of_starting_grip <- time_of_starting_grip[!is.na(time_of_starting_grip)] #gets rid of all the NA, only reports the times where grip starts

letting_go <- NULL
for (i in 1:number_of_observations) {
  if (is.na(REAL_outputs_considered_grip[i])==FALSE & is.na(REAL_outputs_considered_grip[i+1])==TRUE) { #denotes beginning of grip 
    letting_go[i] <- grip_output[i+1]
  }
  else {
    letting_go[i] <- NA
  }  
}
indicies_of_letting_go <- letting_go== grip_output 
time_of_letting_go <- time[indicies_of_letting_go] #gives us the time where the grip ended for each peack
time_of_letting_go <- time_of_letting_go[!is.na(time_of_letting_go)] #gets rid of all the NA, only reports the times where grip lets go
number_of_grips <- length(time_of_letting_go) #should be that the number of letting go= number of grips






###### length of time of letting_go and start_of grip should be either the same or start should be +1 but that is not currently true...



######################################################################
    
  
  start_of_grip[i] <-  ####VALUE 
  end_of_grip[i] <- ###TIME WHERE grip_output<= resting_output #denotes end of grip and records what time that occured
  length_of_grip[i] <- end_of_grip[i]- start_of_grip[i]
  number_of_grips <- length(length_of_grip) #total number of grips per participant


#######    this could be per peak, max, min, median/avg



  

#============================================================================================================
#THESE ARE FOR EACH "GRIP"
#__________________________________________________________________________________________________________________
#max output per grip and when it occurs



#for all the grips that occurs
max_outputs_for_each_grip <- #MAX WITHIN SAID PEAK
indicies_of_max_for_grip <- max_output_of_each_grip==grip_output
time_max_output_of_each_gruo <- time[indicies_of_max_for_grip]
#------------------------
#  how long till maximum ONLY IN PEAK
 #time max was reached minus time grip started
#-----
  #how long after max did they quit ONLY IN PEAK
  #time quit- time max

#===========================================================================================
#rate at which max is reached


  





