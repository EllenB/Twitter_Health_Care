##################################################################################
## https://dev.twitter.com/docs/platform-objects/tweets
## Gives an overview/description of what can be obtained with these data
## CODE TO DOWNLOAD SEVERAL TWEETS
#####################################################################################################
## The first column "created at" refers to the UTC time when the tweet was created.
## We would need the local time of when the tweet was created so we need the time zone/ and
## location.
## This code is from George Fisher and Bill Howe:
## https://github.com/grfiv/healthcare_twitter_analysis/blob/master/code/create_bulkfile.py
## I simplified this code a bit for my own purpose (dropped a few functions e.g.)
## and wrote some extra comments and put in lots of print statements
## This was mainly for my own understanding such that I can understand what
## this excellent written code this.
## This code also uses another program called twitter_credentials.py
## In this code, you need to fill in your api_key, api_secret, access_token_key and access_token_secret
#######################################################################################################

def twitterreq(url, method, parameters):
    """
    Send twitter URL request (URL request meaning the URL you need to use in the API to get the data)  
    Utility function used by the others in this package   
    Note: calls a function twitter_credentials() contained in
          a file named twitter_credentials.py which must be provided as follows:
            api_key = " your credentials "  
            api_secret = " your credentials "  
            access_token_key = " your credentials "  
            access_token_secret = " your credentials "  
            return (api_key,api_secret,access_token_key,access_token_secret)
          
     This function is based on a shell provided by and further adapted by George Fisher (see link above)
     Bill Howe
     University of Washington
     for the Coursera course Introduction to Data Science
     Spring/Summer 2014
    """
    import oauth2 as oauth
    import urllib2 as urllib

    # this is a private function containing my Twitter credentials
    from twitter_credentials import twitter_credentials
    api_key,api_secret,access_token_key,access_token_secret = twitter_credentials()

    _debug = 0

    oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
    oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

    signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

    http_method = "GET"

    http_handler  = urllib.HTTPHandler(debuglevel=_debug)
    https_handler = urllib.HTTPSHandler(debuglevel=_debug)
    
    '''
    Construct, sign, and open a twitter request
    using the hard-coded credentials above.
    '''
    
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                                 token=oauth_token,
                                                 http_method=http_method,
                                                 http_url=url, 
                                                 parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

    headers = req.to_header()

    if http_method == "POST":
      encoded_post_data = req.to_postdata()
    else:
      encoded_post_data = None
      url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)
    
    return response
#############################################################################
## CODE FOR LOOKING UP MULTIPLE TWEETS
#############################################################################

def lookup_multiple_tweets(list_of_tweet_ids):
    
    """
    Ask Twitter for information about 
    a bulk list of tweets by id
    
    the Twitter API for this is here:
    https://dev.twitter.com/docs/api/1.1/get/statuses/lookup
    
    Use: 
    import json
    from twitter_functions import lookup_multiple_tweets


    list_of_tweet_ids = ["473010591544520705","473097867465224192"]
    result = lookup_multiple_tweets(list_of_tweet_ids)
    for foo in result:
        tweetdata_list = json.loads(foo)
        break
    # there must be a better way


    for tweetdata in tweetdata_list:
    print json.dumps(tweetdata, sort_keys = False, indent = 4)
    """
    # https://dev.twitter.com/docs/api/1.1: All this comes from the REST API.
    # REST API means the 
    #print list_of_tweet_ids
    #list_of_tweet_ids
    csv_of_tweet_ids = ",".join(list_of_tweet_ids)
    #print type(list_of_tweet_ids) # Says this is type string while it has to be type list if you try to do it manually
    #print csv_of_tweet_ids
    # The above gives a problem in the command of George or my code. If I run this, I get 
    #import json
    # What the join command does is return a string in which the string elements of sequence have been joined by separator (which equals , here).
    #print csv_of_tweet_ids# this just gives these numbers like: number1, number2, etc
    url = "https://api.twitter.com/1.1/statuses/lookup.json?id=" + csv_of_tweet_ids
    # This is the example from the website: https://dev.twitter.com/docs/api/1.1/get/statuses/lookup
    #url="https://api.twitter.com/1.1/statuses/lookup.json?id=432656548536401920,20"
    #url="https://api.twitter.com/1.1/statuses/lookup.json?id=418170056326270977" ## If you want to run the code 
    # You can also run this with one message at a time
    #https://api.twitter.com/1.1/statuses/lookup.json is the command
    # Go to https://dev.twitter.com/docs/api/1.1/get/statuses/lookup for more information
    # You can get multiple requests (it says maximum 100)
    # See the following link: 
    # This url is the URL of the API to get the required information:
    #https://dev.twitter.com/docs/api/1.1
    #print url
    parameters = []
    #response = "test"
    response = twitterreq(url, "GET", parameters) # This function is written above
    ##for foo in response: #Uncomment if you want to print the data to the screen.
        ##tweetdata_list = json.loads(foo)
        ##break
    ##print tweetdata_list
    #print response
    #for line in response: # This code is added to George code and comes from the code from the class. It basically prints out the
        # the fields what you extract on your screen. If desired you can also write this into a document. Uncomment this line if you want to see this
        # printed on the screen.
        #print line.strip()
    #print response # This does not work
    return response

def parse_AFINN(afinnfile_name):
    """
    Parse the AFIN-111 sentiment file
    
    Input:  afinnfile_name: the [path/] file name of AFIN-111.txt
    
    Output: dicts of:
              sentiment_words: score
              sentiment_phrases: score
            
    Usage: from twitter_functions import parse_AFINN
           sentiment_words, sentiment_phrases = parse_AFINN("AFINN-111.txt")
    """
    import re # regular expression
    afinnfile = open(afinnfile_name)
    
    sentiment_phrases = {}
    sentiment_words   = {}
    for line in afinnfile:
      key, val  = line.split("\t")        
      if " " in key:
        key = re.sub(r"\s{2,}", " ", key) # strip extra whitespace
        sentiment_phrases[key.lower()] = int(val)
      else:
        sentiment_words[key.lower()] = int(val)
    #print sentiment_words # This is the dictionary with the words and the value attached to it
    #print sentiment_phrases
    return (sentiment_words, sentiment_phrases)

if __name__ == '__main__':
  import sys  
  lookup_multiple_tweets(sys.argv[1])
  

    
