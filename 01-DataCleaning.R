##  ---------------------------
##  01-DataCleaning
##
##  Imports the gas exchange data from a pulmonary gas exchange system and preparing it
##  for further analysis.
##  
##  Author: "Nicki lentz"
##  Date: "12/1/2021"
##
##  Email: nickilentz@hotmail.com
## ---------------------------

library(tidyverse)
library(lubridate)
ggthemr::ggthemr("greyscale")


## -- Import and prepare data -- ##

column_names <- c("Time","Oload","HR","VE","BRFEV%", "VO2","VCO2","RER","VO2kg")
#each subject had 8 trials (4 concentric and 4 eccentric)
subject <- c(rep("FP1",8),rep("FP2",8),rep("FP3",8),rep("FP4",8),rep("FP5",8))
contraction <- c(rep("CON",4), rep("EXC",4),rep("CON",4), rep("EXC",4),
                 rep("CON",4), rep("EXC",4),rep("CON",4), rep("EXC",4),rep("CON",4), rep("EXC",4))
#Four intensities (20,40,60,80N) was used for both concentric and eccentric contractions
Load <- c(20,40,60,80,20,40,60,80,20,40,60,80,20,40,60,80,20,40,60,80,
          20,40,60,80,20,40,60,80,20,40,60,80,20,40,60,80,20,40,60,80)

#Imports all the data from a specific directory
path = "../data/rawData/vyn/"
path_allSubjects <- list.files(path = path, pattern = ".csv", full.names = TRUE)
data <- path_allSubjects %>% 
  #first two rows contained meta information which we are not interested in
  map(~data.table::fread(., skip = 2))

for (i in 1:length(data)){
  #Because of technology errors in the pulmonary gas exchange system, the 14th csv file
  #already had the time column as integer where the others
  #were character strings. Therefore, an if statement was made to ignore the
  #change of time column for the 14th csv file.
  
  if (i == 14){
    colnames(data[[i]]) <- column_names
    data[[i]] <- data[[i]] %>% 
      mutate(Subject = subject[[i]],
             Contraction = contraction[[i]],
             Load = Load[[i]],
             #Also recalculating RER as it gave insane high numbers
             RER = VCO2 / VO2) %>% 
      select(-c("Oload","HR","BRFEV%"))
  } else {
    colnames(data[[i]]) <- column_names
    data[[i]] <- data[[i]] %>% 
      mutate(Time = period_to_seconds(ms(Time)),
             Subject = subject[[i]],
             Contraction = contraction[[i]],
             Load = Load[[i]]) %>% 
      select(-c("Oload","HR","BRFEV%"))
  }
  
  #The 34th csv file also had an error, where the VO2 and CO2 columns were characters
  #instead of numeric values.
  if (i == 34){
    data[[i]] <- data[[i]] %>% 
      mutate(VO2 = as.numeric(VO2),
             VCO2 = as.numeric(VO2),
             VO2kg = as.numeric(VO2kg))
  }
  
  #imputating missing values based on the nearest points and weighted by an exponential factor.
  data[[i]] <- imputeTS::na_ma(data[[i]], k = 3, weighting = "exponential")
  
  data.table::fwrite(data[[i]], path_allSubjects[[i]])
  
}
