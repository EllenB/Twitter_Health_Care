##############################################################################
## Analysis of anxiety related tweets
## Ellen Brock
## Date: 25 August 2014
## Code written for course Introduction to Data Science
## This work is part of a project for Saama Technologies based on 
## healthcare related twitter data
## The following code reads in several csv files that each contain data with
## around 39 features. 
## This code:
## 1. Does one exploratory data analysis and cleans up some of the data
## 2. Converts the variables related to the date/time of the tweet of the file 
## into a format R can work with.
## 3. Extract the year, month, day of the week and time of the day from this data variable
## 4. Performs an ANOVA analysis to study whether the sentiment of the tweet
##    (score given in the data before) differs across the month and day of the
##    week. 
##############################################################################
## 1. List the files from a directory and append to one big dataset
##############################################################################
setwd("E:/Ellen/coursera/DataScience2/project/Finished_Files")
filenames <- list.files()
Anxiety = do.call("rbind", lapply(filenames, read.csv, header = TRUE,
                                  stringsAsFactors = FALSE ))
## Write this file into one csv file:
write.csv(Anxiety, file = "E:/Ellen/coursera/DataScience2/project/Anxiety_all.csv", row.names = FALSE)
##############################################################################
## 2. Some summary statistics
##############################################################################
nrow(Anxiety)
summary(Anxiety)
str(Anxiety)
names(Anxiety)
##############################################################################
## 3. Examining the dates and putting them in the right format.
##    All dates are in UTC time, need to be converted to local ime
##    See separate PPT on how to understand/read time of the tweets
##############################################################################
## First I need to convert the character in which the dates are into a data 
## format: Sat Mar 22 15:41:14 +0000 2014
## First from the character, I strip the "+0000" character 20-25:
Anxiety$created_at_new = sub("+0000 ","",Anxiety$created_at)
## One can still see the "+" sign and this needs to be removed too:
Anxiety$created_at_new = gsub("[+]","",Anxiety$created_at_new) 
## Now the date looks something like this e.g.:
## Sat Mar 22 15:41:14 2014
## Now, R needs to understand that this is a date:
## See e.g.: http://en.wikibooks.org/wiki/R_Programming/Times_and_Dates
Anxiety$UTC_Tweet = as.POSIXct(Anxiety$created_at_new, format="%a %b %d %H:%M:%S %Y")
##############################################################################
## 3. Understanding the UTC offset variable.
##############################################################################
## In order to look at the local time, I need to variable UTC_offset
## I first see how many observations are missing in this dataset
## When I try to run the summary command, I see that this is expressed as a 
## character still
## Running the summary statistics, we see that the variable is character.
## and we need to convert it into a numeric variable first.
summary(Anxiety$user_utc_offset)
str(Anxiety$user_utc_offset)
Anxiety$user_utc_offset = as.numeric(Anxiety$user_utc_offset)
summary(Anxiety$user_utc_offset)
#55049 is the number of missing observations in this dataset
# Make a subset of this and then see how many data are there for the location
# variable
Anxiety_NA_UTC =  subset(Anxiety,is.na(Anxiety$user_utc_offset))
v = which(Anxiety_NA_UTC$user_location=="")
length(v) #14228 data points have the user_location also empty
# There is not much with these data we can do, so we need to drop them anyway
head(v)
## Make a frequency table of the different user_locations that are given
## Write it into a csv file for later use to be linked to the MapQuest API
Location_Table = table(Anxiety_NA_UTC$user_location)
Location_Table
write.csv(Location_Table, file = "E:/Ellen/coursera/DataScience2/project/Location_Table.csv", row.names = FALSE)
## When looking at the user_location variable missing records, are there data 
## on the UTC_offset
names(Anxiety)
table(Anxiety$user_time_zone)
## user_time_zone in the dataset does not seem to match with the location 
## specified by the user in some cases
## This needs more clean-up work.
## Subsequently, I will not work with hour but only with day of the week and
## month.
##############################################################################
## 4. Creating separate variables for the month, hour and day of the week.
##############################################################################
## In what follows, I will continue with the record "created_at"
## And extract the month, day of the week, hour and year from this record
DD = strptime(Anxiety$created_at_new, format="%a %b %d %H:%M:%S %Y")
Anxiety$month=DD$mon+1
table(Anxiety$month)
## It is shown in the data that there are even observations from the month July
subset7 <-subset(Anxiety,month==7)
## Upon inspection, we see even data from the earlier years
## Let's create a variable called year:
Anxiety$year = DD$year+1900
table(Anxiety$year) # There are data from 2011 and 2013 in the data which need
## to be removed:
v = which(Anxiety$year==2011|Anxiety$year==2013)
v
length(v) # 67
## Remove these 67 observations:
nrow(Anxiety)
Anxiety = Anxiety[-v,]
nrow(Anxiety)
table(Anxiety$month)
## Now I have data for all the months. The month June is not represented well yet.
## So, I will drop this month.
## I also create a variable that looks at the hour:
ls(DD)
table(DD$hour) # Gives you the number of tweets in the UTC time zone
# Does not make much sense to look at this as people live across time zones.
## I also look at a variable that looks at the day of the week:
DD = strptime(Anxiety$created_at_new, format="%a %b %d %H:%M:%S %Y")
table(DD$wday)
table(weekdays(DD))
Anxiety$DayOfWeek= weekdays(DD)
table(Anxiety$DayOfWeek)
## Next, I drop month six as there are not enough observations:
v = which(Anxiety$month == 6)
v
length(v) # 254
## Remove these 67 observations:
nrow(Anxiety)
Anxiety2 = Anxiety[-v,]
table(Anxiety2$month)
#################################################################################
## 5. Sentiment analysis across the month
#################################################################################
## Create a box plot:
class(Anxiety2$month)
## I will label this as a factor together with the monthly labels:
Anxiety2$month = factor(Anxiety2$month,
                        labels = c("Jan", "Feb", "Mar","Apr","May"))
boxplot(sentiment~month,
        data = Anxiety2,main="Sentiment across January -  May",
        xlab = "Months",ylab = "Sentiment score")
axis(2, at=seq(0,4,1)) 

## Average tweet sentiments per month
tapply (Anxiety2$sentiment,Anxiety2$month,mean)
## Perform and ANOVA analysis (later check also the normality assumptions)
## See: http://www.ats.ucla.edu/stat/r/faq/posthoc.htm
anov1= aov(Anxiety2$sentiment~Anxiety2$month)
summary(anov1)
## Post hoc tests (to see the differences between which months):
TukeyHSD(anov1)
plot(TukeyHSD(anov1))
#################################################################################
## 6. Sentiment analysis across the weekdays
#################################################################################
## Create a box plot:
Anxiety2$DayOfWeek=factor(Anxiety2$DayOfWeek)
boxplot(sentiment~DayOfWeek,
        data = Anxiety2,main="Sentiment across January -  May",
        xlab = "Days",ylab = "Sentiment score")
axis(2, at=seq(0,4,1)) 
tapply (Anxiety2$sentiment,Anxiety2$DayOfWeek,mean)
tapply(Anxiety2$sentiment,Anxiety2$DayOfWeek,median)
## Perform an ANOVA analysis(later also check the normality assumptions)
anov2= aov(Anxiety2$sentiment~Anxiety2$DayOfWeek)
summary(anov2)
## This statistic only says that there is a difference between the different days
## of the week. This does not say between which days there is a difference.
## In order to see between which days of the week there is, run the following
## code:
TukeyHSD(anov2)
plot(TukeyHSD(anov2))


