#!/usr/bin/python3
# Deletes all tweets except those favorited by account holder.
# todo: clean up the arguments to the function, have the dates like in the prepare timeline function. 
# check if the favoriting is working., use the tweet pull var.

import tweepy
import keys
from datetime import datetime
from optparse import OptionParser
import json

import pytz

from dateutil.parser import parse

utc = pytz.UTC

# Connect To Your Twitter Account via Twitter API
auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_SECRET)

api = tweepy.API(auth,
                 wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True,
                 retry_count=3,
                 retry_delay=5,
                 retry_errors=set([401, 404, 500, 503]))


def inspect(id):
    # status = api.get_status(id, tweet_mode="extended")
    status = api.get_status(id)

    # Get whether you have favorited the tweet yourself
    #status_favorited = status._json['favorited']
    status_favorited = status.favorited

    if status_favorited == False:
        print("INSPECT have not favorited")
    else:
        print("INSPECT have favorited")
    print(status.text)
   

def read_twitter_json(file_name):
    """ Read JSON file and returns a json object"""
    with open(file_name, "r") as tweets_file:
        tweets_lines = tweets_file.readlines()
    # Replace header
    tweets_lines[0] = tweets_lines[0].replace('window.YTD.tweet.part0 = ', '')
    # Convert list back to text
    tweets_data = ''.join(tweets_lines)
    # Parse JSON twitter data
    tweets_js = json.loads(tweets_data)
    return tweets_js

def tweet_decode(tweet):
    """ Gets data from tweet and returns a simplified data structure
        tweet = {
            'full_text': 'This is a tweet #hello #world http://t.co/13456',
            'urls': [ 'http://en.wikipedia.org/' ]
            'hashtags': [ '#hello', '#world' ]
        }
    """
    tweet_simple = {}
    # Get data from tweet
    tweet_simple['id'] = tweet['tweet']['id']
    tweet_simple['full_text'] = tweet['tweet']['full_text'] # Text
    tweet_simple['created_at'] = tweet['tweet']['created_at'] # Text

    return tweet_simple

def print_tweet(tweet):
    print("\"\"\"{}\"\"\"".format(tweet['full_text']))

def sort_archive():
    parser = OptionParser()
    parser.add_option("-s", "--date-start", dest="date_start",
                  help="Start date to sort the archive", metavar="DATE_START")
    parser.add_option("-e", "--date-end", dest="date_end",
                  help="End date to sort the archive", metavar="DATE_END")
    parser.add_option("-f", "--file", dest="filename",
                  help="Path to Twitter JSON archive.", metavar="FILENAME")
    
    (options, args) = parser.parse_args()

    if not(options.filename):
        print("You need to enter a filename; exiting.")
        return

    base_filename = ""

    if (options.date_start and options.date_end):
        base_filename = options.date_start + "_to_" + options.date_end
    
    keep_filename = "archive-keep" + base_filename + ".js"
    delete_filename = "archive-delete" + base_filename + ".js"

    keep_write = open(keep_filename, 'w')
    delete_write = open(delete_filename, 'w')
    
    keep_write.write("window.YTD.tweet.part0 = [")
    delete_write.write("window.YTD.tweet.part0 = [")

    # Validate dates
    if (options.date_start):
        date_start = utc.localize(parse(options.date_start))
    if (options.date_end):
        date_end = utc.localize(parse(options.date_end))

    ## Read Twitter file (JSON format)
    tweets_js = read_twitter_json(options.filename)
    
    first_tweet_keep = True
    first_tweet_delete = True

    ## Loop over tweets
    for tweet in tweets_js:
        # Decode tweet in a simple structure
        tweet_simple = tweet_decode(tweet)

        # print('\n  New Tweet\n ', tweet_simple['id'])
       
        tweet_datetime = parse(tweet_simple['created_at'])

        if options.date_start:
            if tweet_datetime <= date_start:
                continue
        if options.date_end:
            if tweet_datetime >= date_end:
                continue
        
        id = tweet_simple['id']
        status = api.get_status(id)   

        # Get whether you have favorited the tweet yourself,
        # using the current status, not archive status.
        status_favorited = status._json['favorited']

        status_date = tweet_datetime.strftime('%a %b %d %H:%M:%S %Y')
        print(status_date, 'Examining', id, ' favorited : ', status_favorited)

      	
        if status_favorited == False:
            #print("not favorited")
            if (first_tweet_delete == False):
                delete_write.write(",")

            json.dump(tweet_simple, delete_write, indent = 4, sort_keys=True)
            
            if (first_tweet_delete):
                first_tweet_delete = False
        else:
            #print("favorited")
            if (first_tweet_keep == False):
                keep_write.write(",")
            json.dump(tweet_simple, keep_write, indent = 4, sort_keys=True)
           
            if (first_tweet_keep):
                first_tweet_keep = False

    
    keep_write.write("]")
    delete_write.write("]")

    keep_write.close()
    delete_write.close()


# Run main function
if __name__ == '__main__':
    sort_archive()


