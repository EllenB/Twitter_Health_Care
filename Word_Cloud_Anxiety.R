############################################################################
## This code shows a word cloud
##
## This code is based on:
## 
## http://www.rdatamining.com/examples/text-mining
## http://www.rdatamining.com/docs
## http://www.analyticsvidhya.com/blog/2014/05/build-word-cloud-text-mining-tools/
##
############################################################################
## 1. Set working directory and read in the data
############################################################################
setwd("E:/Ellen/coursera/DataScience2/project")
Anxiety <- read.csv("Anxiety_cleaned.csv")

## My computer cannot handle such a big dataset and keeps on hanging
## I randomly sample 50 000 tweets just to illustrate the code

Sample <- Anxiety[sample(1:nrow(Anxiety), 50000,
                          replace=FALSE),] 

nrow(Sample)

rm(Anxiety) # To clear some memory
#############################################################################
## 2. Create a corpus, clean up the data and build a word cloud.
#############################################################################
## Install and/or load the required packages
##
library(tm)
# Build a corpus, which is a collection of text documents
myCorpus <- Corpus(VectorSource(Sample$content))
## I remove the Anxiety variable to create some free space:
rm(Anxiety)
## Put all words into lower case
myCorpus <- tm_map(myCorpus, tolower)
## Remove punctuation
myCorpus <- tm_map(myCorpus, removePunctuation)
## Remove numbers
myCorpus <- tm_map(myCorpus, removeNumbers)
## Remove stopwords
## In order to see what the stop words are, type the following command:
stopwords()
myCorpus <- tm_map(myCorpus, removeWords, stopwords())
## Remove white space
myCorpus <- tm_map(myCorpus,stripWhitespace)
## Inspect the corpus:
inspect(myCorpus[1:3])
##Build the word cloud:
library(wordcloud)
wordcloud(myCorpus, min.freq=500, random.order=FALSE)
# min.freq is the minimum times the word needs to appear before it comes into the 
# cloud



