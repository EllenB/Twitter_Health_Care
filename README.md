Twitter_Health_Care
===================

This repository gives *some* of the code I have written for the optional project with Saama Technologies organised throught the Coursera course Introduction to Data Science.

The following files are added to this Github repository:

- ** Write_To_Output10**: This is code that takes one CSV file and creates extra records by doing a call to the Twitter API. This code is fully obtained from the code of George Fisher: https://github.com/grfiv/healthcare_twitter_analysis. The program is simplified such that one CSV at a time is processed, code is commented out and extra print statements are given when trying to understand/experiment with the code. The code is using the Google API for the location variables but has a limit of 2500 tweets per day. All errors are mine in this code.

- **Twitter_Test3**: Uses helper functions for the Twitter API and is obtained from the code of George Fisher.

- **twitter_credentials**: You need to type in your keys before you can run the Python codes above. This code is obtained from Bill Howe and George Fisher. This code needs to be in the same directory as the code Write_To_Output10 and Twitter_Test3.

- **ANOVA_Analysis.R**: This file reads in processed tweets (with about 39 features) and does an ANOVA analysis on these tweets using day of the week, month and later on hour of the day.

- *Project_Anxiety_Ellen_9_ Sept_2014_Interim_1_short*: R Markdown file (output) of the ANOVA_Analysis code in pdf format.

- **HozBarPlot.R**: This code is for creating a horizontal bar plot showing the Top 20 authors of the tweet. The results is in a pdf file using a similar name.

- **Word_Cloud_Anxiety.R**: Code to create a word cloud based on a sample of the data (about 50 000 tweets). The output is given in a JPEG file. 

 
