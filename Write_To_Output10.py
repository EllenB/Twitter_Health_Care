#######################################################################################################################
## This code is obtained from the Github account from George Fisher:
## https://github.com/grfiv/healthcare_twitter_analysis/tree/master/code
## I restructured and simplified this a bit for my own use and added some comments
## and print statements (commented out)
## for my own understanding.
## In contrast to the original code, I run the code only for one CSV file at a time so I could drop some outer loop.
## I also start with the helper functions first which make calls to other files as well (see documente below) and which
## are also obtained from the code of George Fisher.
## In order to run this code, go to the command line and type in:
## python Write_To_Output "File_You_Want_To_Process.csv"
## For the processing/imputation of user_location data, the Google API is used.
## However, there is a maximum of 2500 downloads per day.
## In the next steps, I will:
## a) Explore the MapQuest code written by George
## b) Also use the json version of this code and comment/structure it in a similar way how I have done it below for my
##    own understanding. 
#######################################################################################################################
## HELPER PROGRAMS
#######################################################################################################################
def parse_tweet_json(line, tweetdata):
    """
    Take in a line from the file as a dict
    Add to it the relevant fields from the json returned by Twitter
    
    Documentation https://dev.twitter.com/docs
    """
    import time
    import datetime
    #print tweetdata
    #print tweetdata.keys()
    #print type (tweetdata) # This is a dictionary

    ####
    ## To get the created_at record
    #####

    line["created_at"] = str(tweetdata["created_at"]) # Variable 
    #print "LINE"
    #print line                         
    
    line["tweet_coordinates"]  = str(tweetdata["coordinates"])
    #print "LINE"
    #print line
    # unix timestamp...better for sorting, searching, indexing
    line["tweet_timestamp"] = "" # This creates on extra record in this 
    #print "LINE"
    #print line
    try:
        line["tweet_timestamp"] = str(time.mktime(datetime.datetime.strptime(line['firstpost_date'], "%m/%d/%Y").timetuple()))
    except:
        try:
            line["tweet_timestamp"] = str(time.mktime(datetime.datetime.strptime(line['firstpost_date'], "%m/%d/%y").timetuple()))
        except:
            pass
        
    line["tweet_favorited"]    = str(tweetdata["favorited"])
    if tweetdata["entities"] is not None:
         if tweetdata["entities"]["hashtags"] is not None:
             hashtag_string = ""
             for tag in tweetdata["entities"]["hashtags"]:
                 hashtag_string = hashtag_string + tag["text"] + "~"
             hashtag_string = hashtag_string[:-1]
             line["hashtags"] = str(hashtag_string.encode('utf-8'))
         else:
             line["hashtags"] = ""
         if tweetdata["entities"]["user_mentions"] is not None:
             user_mentions_string = ""
             for tag in tweetdata["entities"]["user_mentions"]:
                 user_mentions_string = user_mentions_string + tag["screen_name"] + "~"
             user_mentions_string = user_mentions_string[:-1]
             line["user_mentions"] = str(user_mentions_string)
         else:
             line["user_mentions"] = ""
    line["tweet_retweet_count"]  = str(tweetdata["retweet_count"])
    line["tweet_favorite_count"] = str(tweetdata["favorite_count"])
    line["tweet_retweeted"]      = str(tweetdata["retweeted"])
    line["tweet_place"]          = str(tweetdata["place"])
    line["tweet_geo"]            = str(tweetdata["geo"])
    line["tweet_coordinates"]    = str(tweetdata["coordinates"])
    line["tweet_in_reply_to_screen_name"]    = str(tweetdata["in_reply_to_screen_name"])
    if tweetdata["user"] is not None:
        line["user_friends_count"]    = str(tweetdata["user"]["friends_count"])
        line["user_name"]             = tweetdata["user"]["name"].encode('utf-8')
        line["user_favourites_count"] = str(tweetdata["user"]["favourites_count"])
        line["user_screen_name"]      = tweetdata["user"]["screen_name"].encode('utf-8')
        line["user_listed_count"]     = str(tweetdata["user"]["listed_count"])
        line["user_location"]         = tweetdata["user"]["location"].encode('utf-8')
        line["user_utc_offset"]       = str(tweetdata["user"]["utc_offset"])
        line["user_followers_count"]  = str(tweetdata["user"]["followers_count"])
        line["user_listed_count"]     = str(tweetdata["user"]["listed_count"])
        line["user_lang"]             = tweetdata["user"]["lang"].encode('utf-8')
        line["user_geo_enabled"]      = str(tweetdata["user"]["geo_enabled"])
        line["user_time_zone"]        = str(tweetdata["user"]["time_zone"])
        line["user_statuses_count"]   = str(tweetdata["user"]["statuses_count"])
        line["user_verified"]         = str(tweetdata["user"]["verified"])
        line["user_description"]      = tweetdata["user"]["description"].encode('utf-8')
    #print "TYPE"
    #print type(tweetdata) # This is a dictionary
    #print tweetdata.keys()
    #print "LINE"
    #print tweetdata["text"].encode('utf-8')
    #print tweetdata["user"]
    #print tweetdata["place"]
    #print "LOCATION"
    #print tweetdata["user"]["location"]
    #print tweetdata["place"]# It all prints "None"
    #print type(tweetdata)
    #print line
    #print type(line) # This is a dictionary
    #print line.keys()

    # geo location data (this API can only process 2500 lines per day. To be extended to the MapQuest API later on)
    from pygeocoder import Geocoder
    try:
        geo_results = Geocoder.geocode(line["user_time_zone"])
        #print "GEOCODER"
        #print line["user_time_zone"] # If there is no time zone and/or user_utc_offset, it prints "Nenjiang River China"
        #print line["user_utc_offset"] # See e.g. Portland Oregan
        #print geo_results
    except:
        geo_results = "error"
    line["user_time_zone_coordinates"] = ""
    line["user_time_zone_placename"]   = ""
    if geo_results != "error":
        line["user_time_zone_coordinates"] = geo_results.coordinates
        for foo in geo_results:
            line["user_time_zone_placename"] = foo
            break
    try:
        geo_results = Geocoder.geocode(line["user_location"])
    except:
        geo_results = "error"
    #print "COORDINATES"
    line["user_location_coordinates"] = ""
    line["user_location_placename"]   = ""
    if geo_results != "error":
        line["user_location_coordinates"] = geo_results.coordinates
        #print line["user_location_coordinates"]
        for foo in geo_results:
            line["user_location_placename"] = foo
            #print line["user_location_placename"]
            break
        
    return line

def find_sentiment(tweet_data, sentiment_words, sentiment_phrases):
    import re
    
    content = tweet_data['text'].lower()
    #print "CONTENT"
    #print content.encode('utf-8') # This prints out the text of the tweet in lower case

    # remove URLs
    content = re.sub(r"\b((?:https?|ftp|file)://[-A-Z0-9+&@#/%?=~_|$!:,.;]*[A-Z0-9+&@#/%=~_|$])", "", content, 0, re.IGNORECASE) 

    # remove hashtags
    content = re.sub(r"#(\w+)", "", content, 0)

    # remove users mentioned
    content = re.sub(r"@(\w+)", "", content, 0)

    # strip out extra whitespace in the remaining text
    content = re.sub(r"\s{2,}", " ", content)
    
    #print content.encode('utf-8')

    words   = content.split()
    #print sentiment_words.keys()

    AFINN_score = 0
    # single words
    for word in words:
        #print "Hello"
        if word in sentiment_words:
            AFINN_score += sentiment_words[word]
            #print word
    #print AFINN_score
    for phrase in sentiment_phrases:
        if phrase in content:
            AFINN_score += sentiment_phrases[phrase]
    #print AFINN_score
    return AFINN_score

def sleep_process(output_dict, output_filename, first_sleep):
    import time
    import sys
    import datetime
    from datetime import timedelta
    
    process_output_file(output_dict, output_filename, first_sleep)
    
    length_of_sleep = int(15.1*60)  # seconds
    timenow    = datetime.datetime.today().strftime("%H:%M:%S")
    timeplus15 = (datetime.datetime.today()+timedelta(seconds=length_of_sleep)).strftime("%H:%M:%S")
    print "sleeping at %s, will resume at %s"%(timenow, timeplus15)
    sys.stdout.flush()
    
    time.sleep(length_of_sleep)
    
def process_output_file(output_dict, output_filename, first_sleep):
    # output_dict basically refers to the list where each item is a dictionary (tweet). This is equivalent to the lines dictionary that
    # has been created below.
    import csv
    import datetime
    if first_sleep:
        #print "Hello"
        first_sleep = False
        f = open(output_filename,'wb')#this is the bigtweet_file.csv file specified below
        # Open this particular file and 'wb' means that Opens a file for both writing and reading in binary format.
        #Overwrites the existing file if the file exists. If the file does not exist, creates a new file for reading and writing.
        # See: http://www.tutorialspoint.com/python/python_files_io.htm
        w = csv.DictWriter(f, delimiter=",", fieldnames=output_dict[0].keys())
        w.writeheader()
        w.writerows(output_dict)
        f.close()
    else:
        f = open(output_filename,'a')
        w = csv.DictWriter(f, delimiter=",", fieldnames=output_dict[0].keys())
        w.writerows(output_dict)
        f.close()
    output_dict = []
    timenow     = datetime.datetime.today().strftime("%H:%M:%S")
    print "%s processed at %s"%(output_filename, timenow) 
#######################################################################################################################
## MAIN PROGRAM
#######################################################################################################################
def Test_Files(input_filename):
    # Import the following packages
    # The package "six" was not installed.
    # I learned how to import packages using the following link:
    # http://www.wikihow.com/Install-Python-Packages-on-Windows-7
    
    import csv
    import json
    import re
    import time
    import sys
    import six
    import datetime

    # Call to other functions written by George Fisher which I simplified slightly and adapted for my own use:
    # https://github.com/grfiv/healthcare_twitter_analysis/tree/master/code
    # This is in a separate python file and needs to be installed in the same directory of this program
    from Twitter_Test3 import lookup_multiple_tweets
    from Twitter_Test3 import parse_AFINN
    
    process_start = datetime.datetime.now() # Prints out the current time
    print "\n================================"
    print "process start: %s"%process_start.strftime("%c")
    print "================================\n"

    ## Create one big output master file that will contain all the data

    output_filename   = "bigtweet_file" + ".csv"
    #print output_filename # You get something like bigtweet_file.csv printed on the screen.
    
    step              = 100 # we're going to process in groups of "step". 100 is the maximum number of messages that you can call through the API in one shot
                            # in your program.
    bulk_list         = []  # batch of rows from input file.  
    list_of_tweet_ids = []  # tweet ids of these rows, this is a list. Based on this, you can invoke the API to extract the other data
    output_dict       = []  # list of dicts to send to output file ## PROBABLY ONE ERROR HERE, THIS FILE DOES NOT GET FILLED UP (see below)
                            # and the call to the function. Should and empty dictionary also not have a {} instead? XXXX

    # the Twitter rate limits are documented here
    # https://dev.twitter.com/docs/rate-limiting/1.1/limits
    ############################################################################################################
    sleep_batch       = 13500 # we sleep after this many lines processed
    #sleep_batch        = 99 # Here we will set this equal to 100 for this program
    sleep_batch_rows  = 0     # the number of lines we've processes since the last sleep
    
    first_sleep       = True               # first time through, we write an output_file header. After the first run this variable is set equal to zero. This is
                                            # useful for the first header function above in the helper functions.
    invalid_json      = False              # in case Twitter sends us junk
    skip_counter      = 0                  # how many rows did we skip because Twitter didn't send us info
    ########################################################
    ## AFIN PROCESSING #####################################
    ########################################################
    # AFINN-111.txt file has to be in the same directory as the directory you have this program in
    ## This is the file that was used for the first assignment
    sentiment_words, sentiment_phrases = parse_AFINN("AFINN-111.txt") ## This is the code that is written in the "Twitter_functions.py" program
    ## NEED TO FIGURE OUT THIS CODE STILL
    
    # read each file in and process it
    # ==================================   
    # open an input file
    print input_filename # This input_filename is one of the arguments of your function. In my case, this a CSV file such as "Anxiety_100.csv". This is also the file
    # you give into the command line where you invoke the program.
    #infile = open(input_filename,"rb")
    #print infile
    infile = open(input_filename, "rb" )# rb means r for only read and b for opening in binary mode see: https://docs.python.org/2/tutorial/inputoutput.html
    #print infile
    reader     = csv.DictReader(infile) # http://java.dzone.com/articles/python-101-reading-and-writing
                                        # Each line is a dictionary
    lines      = list(reader) # list of all lines/rows in the input file
    totallines = len(lines)   # number of lines in the input file
    print totallines # 100
    #print type(lines) # This is a list
    print lines[0] # gives the first tweet
     #print type(lines[0]) # Shows that this is a dictionary
    #print lines[0].keys() # This gives back the keys that are in the dictionary. The first element is the first tweet that has firstpost_date, url, etc as the keys        

    print "\n--Processing of %s rows %d"%(input_filename,totallines)
    
    # read the input file line-by-line
    # ================================
    for linenum, row in enumerate(lines): #https://docs.python.org/2.3/whatsnew/section-enumerate.html        
        #print linenum
        #print row # This gives the actual tweet
        #print type(row) # This is a dictionary
        ########################################################################################################
        # If you have a cutoff here, you need to get the program to:
        # write everything to the disk in a csv and go to sleep. In this program, we have set this equal to 99
        # to make it run once the line touches 100.
        ########################################################################################################

        sleep_batch_rows+=1
        #print sleep_batch_rows
        #### Here the loop to write to the file
        ####################
        if sleep_batch_rows > sleep_batch:
             # UNTIL you reach the batch limit, you keep on adding to a file called output_dict 
             #print "hello"
             print "sleeping after %d lines of file"%(linenum)
             sleep_batch_rows = 0 # set this again equal to zero before you run the next batch (ultimately a batch consists of 13 500 lines)
             sleep_process(output_dict, output_filename, first_sleep)
             ##########################################################
             ## CODE HERE TO WRITE TO A CSV FILE (Big Tweet file)
             ####################################################

                  
        ### THIS GOES INTO THE FILE TO WRITE IT OFF, NEED TO SEE EXACT POSITION
        ##output_dict.append(line)
        tweet_id  = row['url'].split("/")[-1]
        #print row['url'] # This print out something like this for each record: http://twitter.com/cheryljanecky/status/418170056326270977
        #print tweet_id #418170056326270977
        # based on the "/" see: http://www.pythonforbeginners.com/python-strings/python-split/
        #print type(tweet_id_test) # This is a list
        #print tweet_id_test
        # "[-1]" means you will take the last element of this list

        # make sure tweet_id is actually numeric
        if re.match(r"^\d+", tweet_id):
            #^ means match the beginning of the string
            # Successful match at the start of the string
            # https://docs.python.org/2/library/re.html, \d refers to the unicode
            # Successful match at the start of the string
            row['id'] = tweet_id
            # this key gets is the tweet_id you have just extracted.
            #print row['id']
            #print row
            bulk_list.append(row)# Add this new row with the new key 'id' and its value to the bulklist which is a list with all these "new" rows added to it
            #print bulk_list # This gives the entire data into the list with each element a dictionary
            list_of_tweet_ids.append(tweet_id)# This just appends all the tweet_ids (to be called through API to get all the other fields of the tweets
            #print list_of_tweet_ids 
        else:
            print "tweet url terminated with non-numeric in line %d"%(linenum+1)
            print row['url']
            #print bulk_list # Gives all the tweets as a list with each element one tweet and each element is then a dictionary
            # You see that id is addes as one extra record 
            #print list_of_tweet_ids # is a list with all these tweet ids
            #print type(list_of_tweet_ids)

        # if batch-size reached, process the batch
        #print len(bulk_list)
        #print step
        #print(linenum)
        #print totallines

        #print list_of_tweet_ids # This is in the order of the csv file
                
        if len(bulk_list) >= step or (linenum+1) >= totallines: # So here the file will also get processed
        # make a batch request to Twitter 
        # ===============================
            while True: # Changed code here a bit
                result = lookup_multiple_tweets(list_of_tweet_ids)
                if result: break
                print "\nTwitter returned an empty result\n"
                time.sleep(1)
                
            list_of_tweet_ids = [] # Set this again to process the next batch
            
            for foo in result:
                #print foo # prints out the entire dataset
                try:
                    tweetdata_list = json.loads(foo)#The json.loads() function takes a JSON string and returns it as a Python data
                                             #structure.
                    break
                except ValueError, e:
                    print "\nTwitter returned invalid json"
                    print e
                    print "after %d lines of file"%(linenum)
                    bulk_list = []
                    invalid_json = True
                    break
            if invalid_json:
                invalid_json = False
                break

            # tweetdata_list gives all the tweet information you got through the API    
            #print tweetdata_list[0] 
            #print len(tweetdata_list)
            
            if 'errors' in tweetdata_list:
                print "Twitter returned an error message:"
                print "message: " + str(tweetdata_list["errors"][0]['message'])
                print "code:    " + str(tweetdata_list["errors"][0]['code'])
                print "after %d lines of file"%(linenum)
                sleep_batch_rows = 0
                sleep_process(output_dict, output_filename, first_sleep)
                bulk_list = [] # we lose the batch
                continue
            # Twitter's response is in arbitrary order and doesn't necessarily
            # contain a response for every id we requested
            #
            # So we create a dictionary for the tweetdata_list
            # associating id's with their position in the list
            # and a list of id's for searching

            #print tweetdata_list[1]
            #print list_of_tweet_ids # This is empty here
            
            tweet_id_dict = {}
            tweet_id_list = []

            ##################################
            # find every id in tweetdata_list and its position
            for i in range(len(tweetdata_list)):
                #print i # prints out 0 to 9
                #print tweetdata_list[i]['id'] # If you look at this list, the order is different than the order of the original data
                # The order here is (last two digits): 77,40,08,45,81,88,76,80,36,32
                id = str(tweetdata_list[i]['id'])
                #print id
                tweet_id_dict[id] = i # This prints the order how Twitter has downloaded the data
                #print tweet_id_dict
                tweet_id_list.append(id)
                #print tweet_id_list

            batch_process_count = 0
            ##############################
            for line in bulk_list:
                # bulklist is the original file of what you will process and the order of the ids is how you have gotten the original csv file
                if line['id'] not in tweet_id_list: 
                    skip_counter+=1 
                    # check the entire line['id'] is numeric 
                    if re.match(r"^\d+", line['id']): 
                        # yes 
                        print "%d skipped id %d"%(skip_counter, int(line['id'])) 
                    else: 
                        # no 
                        print skip_counter 
                        print "line['id'] is not all numeric" 
                        print line['id']                                
                    continue
                
                #print line['id'] # This will print the value of the ID that is associated with that particular line
                #print tweet_id_dict # This prints the dictionary where the key is the ID and the value is the order in which Twitter has downloaded/processed
                                    # the data
                #print tweet_id_dict[line['id']] # This prints for the original data where they are located in the data downloaded from Twitter.
                # Example: Take the file where we have downloaded the first 10 observations of the anxiety file. The last two digits of the IDs of the URL are
                # (this comes under variable name "url" of the original CSV files. The last two digits of the original first 10 records are:
                # 77,32,36,45,08,88,80,40,81,76
                # The order how Twitter has downloaded the data: 77,40,08,45,81,88,76,80,36,32
                # This command line prints out 0,9,8,3,2,5,7,1,4,6
                #print tweetdata_list # Gives all the data you got through the API call and also in that order according Twitter has processed it. 
                tweetdata = tweetdata_list[tweet_id_dict[line['id']]]
                #For tweetdata, the API related data are loaded into the tweetdata and the order is maintained of the original data
                #print "new ID"
                #print line['id']
                #print tweetdata['id'] # This prints in the order of the original data and so this needs to match
                # if you take the but for some cases the lines where it is not processed it will print out something different.
                
                if str(line['id']) != str(tweetdata['id']):
                    #print "Hello"
                    # This will print out these IDs that do not match for some reason or the other.
                    skip_counter+=1 
                    print "id mismatch, skipping %d"%(skip_counter) 
                    print "line  id %s"%(str(line['id'])) 
                    print "tweet id %s"%(str(tweetdata['id'])) 
                    continue
                    
                # parse Twitter's response
                # The following to lines I will not need as I do not use the file_counter (I have only one file)
                # and I am also not using the short_file_name
                #line["file_counter"]    = file_counter 
                #line["short_file_name"] = short_file_name

                ### PARSE ALL THE DATA
                # This means that we use all the raw data that we obtained from Twitter will obtain this and put this
                # into a Python dataset such that eventually you will write this into a csv dataset.
                # The parse_tweet_json is obtained through a helper function

                line = parse_tweet_json(line, tweetdata)
                # line here is the line, specific twitter message
                # tweetdata is the raw twitter data and is order according the original order of the CSV file
                # line is made into the order in which the original data in the CSV file are (see print "LINE" statement below)
                # The function parse_tweet_json is a helper function (see above)
                ## Compute the sentiment for this particular tweet
                line['sentiment'] = find_sentiment(tweetdata, sentiment_words, sentiment_phrases)
                #print line['sentiment']
                # tweetdata is the raw data on how you extracted them.
                #sentiment_words and sentiment_phrases are things you have computed above.

                #print tweetdata
                #print "LINE"
                #print line
                #print "Sentiment"
                #print line["sentiment"]
                output_dict.append(line)
                batch_process_count+=1

                #print output_dict # This is in the order of the original
                # csv raw data files
            #print "test_output_dict"
            #print output_dict

            print "Rows processed: " + str(len(output_dict))
            bulk_list = [] # You have to set this again to zero as you
            # will need to process the next batch from scratch

    #print output_dict# This file needs to go into the parsing to process it.             
    # Process the file for the last time or when the data is pretty small            
    process_output_file(output_dict, output_filename, first_sleep)

    # how long did it take?
    process_end     = datetime.datetime.now()
    process_elapsed = process_end - process_start
    process_seconds = process_elapsed.seconds
    process_minutes = process_seconds/60.0
    process_hours   = process_minutes/60.0

    print "\n================================"
    print "process start: %s"%process_start.strftime("%c")
    print "process end:   %s"%process_end.strftime("%c")
    print "process elapsed hours %0.2f"%process_hours
    print "================================\n"
     
if __name__ == '__main__':
    import sys
    Test_Files(sys.argv[1])




