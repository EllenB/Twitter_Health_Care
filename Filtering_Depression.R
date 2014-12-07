#################################################################################
## This code filters out the tweets those tweets written by people who suffer
## from a mental health disease (here anxiety)
## from the raw data containing all data that have the hash tag "anxiety"
## 
## Other clean-up tasks are also performed with these data.
## The program is related to the anxiety related tweets only and can be
## extended for other mental health diseases.
##
## As a first step, I first filter out some twitter accounts who are of
## promotional nature. 
##
## Author: Ellen Brock
## Date: 1 August 2014
##################################################################################
##################################################################################
## 1. Setting the working directory and reading in the data
##################################################################################
setwd("E:/Ellen/coursera/DataScience2/project/depression")
Big = read.csv("Tweets_Depression.csv",stringsAsFactors = FALSE)
nrow(Big) #356654
names(Big)
##################################################################################
## 2. Inspecting the data and some clean-up
##################################################################################
## a. Converting the firstpost_date into an R format and creating an observation
## for the year and month out of this.
## See e.g.: e.g.: http://en.wikibooks.org/wiki/R_Programming/Times_and_Dates
## Once I have filtered all the users who suffer from anxiety disorders, I 
## will also need to create variables related to the hour and time of the week.
class(Big$firstpost_date) #character
## The format is little bit different than the format of the previous files

Big$Date = as.POSIXct(Big$firstpost_date, format="%m/%d/%y")

DD = strptime(Big$firstpost_date, format="%m/%d/%y")
#ls(DD) "hour"  "isdst" "mday"  "min"   "mon"   "sec"   "wday"  "yday"  "year" 
Big$month=DD$mon+1
Big$year = DD$year+1900
## b. Frequency table for year
table(Big$year)
#2009   2010   2011   2012   2013 
#3      1      8     96 356511 
## Only retaining the data from 2013
v = which(Big$year==2009|Big$year==2010|Big$year==2011|Big$year==2012)
v
length(v)#108
Big = Big[-v,]
nrow(Big) #356546
table(Big$month)
#################################################################################
## 3. A lot of the data are of "promotional" nature and could be deleted. I clean 
##    up the data by looking who are the main contributors to anxiety related 
##    tweets
#################################################################################
Top_Tweeters <- table(Big$trackback_author_nick)
#plot(sort(Top_Tweeters,decreasing=TRUE)[1:5]),type="h")
Top20 <- sort(Top_Tweeters,decreasing=TRUE)[1:20]
Top20
df=as.data.frame.table(Top20)
names(df)
names(df) <- c("Author", "Count")
## Creating a horizonel bar plot
library(ggplot2)
ggplot(df, aes(x=Author, y=Count))+ geom_bar(stat="identity") + coord_flip() +
  xlab("Authors") + ylab("Count")

## You could to the same with the URL links as this will be better to investigate
Top_Tweeters2 <- table(Big$trackback_author_url)
Top20_2 <- sort(Top_Tweeters2,decreasing=TRUE)[1:20]
Top20_2
## One group is a forum which I will retain together with three other authors,
## the rest of the top 20 I will delete
## The following people were filtered out:
nrow(Big)
#http://www.ats.ucla.edu/stat/r/modules/subsetting.htm
# Put the authors you want to drop in a list:
Author_List <- c("mindfultherapy4","daniel_l_baker","ahealthblog","drdaveanddee",
                 "healthyplace","therapyforum","brittaneinast","manurananayakka",   
                 "krisamelong","antistigma","creativechange1","insightmanager",
                "mindfulnessman","quoteninstagram")
BigNew <- Big[!(Big$"trackback_author_nick" %in% Author_List), ]
nrow(BigNew)#325399
#################################################################################
## 4. Running regular expression searching in the "content" for terms like
##    "diagnosed" and "suffer"
#################################################################################
names(BigNew)
diagnosedNew <- grep ("[Dd]iagnosed",BigNew$content)
length(diagnosedNew) #722 observations
sufferNew <- grep("[Ss]uffer", BigNew$content)
length(sufferNew) # 6303
## Do the same but on the original dataset
diagnosedRaw <- grep ("[Dd]iagnosed",Big$content)
length(diagnosedRaw) #744
sufferRaw <- grep("[Ss]uffer", Big$content)
length(sufferRaw) # 9547
## Write these two datasets into a separate CSV file:
DiagNew = BigNew[diagnosedNew,]
write.csv(DiagNew, file = "E:/Ellen/coursera/DataScience2/project/depression/DiagNew.csv", row.names = FALSE)
SufferNew = BigNew[sufferNew,]
write.csv(SufferNew, file = "E:/Ellen/coursera/DataScience2/project/depression/SufferNew.csv", row.names = FALSE)
DiagRaw=Big[diagnosedRaw,]
write.csv(DiagRaw, file = "E:/Ellen/coursera/DataScience2/project/depression/DiagRaw.csv", row.names = FALSE)
SufferRaw=Big[sufferRaw,]
write.csv(SufferRaw, file = "E:/Ellen/coursera/DataScience2/project/depression/SufferRaw.csv", row.names = FALSE)