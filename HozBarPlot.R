##############################################################################
## This code creates a horizontal bar plot.

## I take some CSV file that I have obtained from Saama Technologies
## containing tweets on anxiety. The code below is based on the raw files that
## are provided by Saama Technologies. 
## Subsequently, select those people/organisations that tweet the most (Top 20).
## Subsequently, I make a horizontal bar plot of these Top 20 contributors.

## Author: Ellen brock
## Date: 8 September 2014

###############################################################################
## Setting the working directory and reading in the CSV file:
setwd("E:/Ellen/coursera/DataScience2/project")
Big = read.csv("Tweets_Anxiety.csv",stringsAsFactors = FALSE)
nrow(Big)
names(Big)

Top_Tweeters <- table(Big$trackback_author_nick)

Top20 <- sort(Top_Tweeters,decreasing=TRUE)[1:20]
Top20
df=as.data.frame.table(Top20)
names(df)
names(df) <- c("Author", "Count")
## Creating a horizonel bar plot
library(ggplot2)
bp <- ggplot(df, aes(x=Author, y=Count))+ geom_bar(stat="identity") + coord_flip() +
  xlab("Authors") + ylab("Count")
bp + ggtitle("Top 20 authors of anxiety related tweets")


