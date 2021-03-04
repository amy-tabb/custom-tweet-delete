#!/usr/bin/python3

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
    tweet_simple['datetime'] = parse(tweet_simple['created_at']) # Parse date to datetime

    return tweet_simple

def print_tweet(tweet):
    print("\"\"\"{}\"\"\"".format(tweet['full_text']))

def wipe_from_file():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                  help="Path to Twitter JSON archive.", metavar="FILENAME")
    
    (options, args) = parser.parse_args()

    if not(options.filename):
        print("You need to enter a filename; exiting.")
        return

    ## Read Twitter file (JSON format)
    tweets_js = read_twitter_json(options.filename)

    print("Confirming that you want to delete the tweets in file ", options.filename)
    print("Number of tweets is ", len(tweets_js))
    
    go_forward = input("Enter 1 to go forward with the delete, any other to exit.")
    
    if (go_forward == '1'):

        ## Loop over tweets
        for tweet in tweets_js:
            
            print('\n  Deleting tweet ', tweet['id'])
       
            id = tweet['id']
            api.destroy_status(id)
    else:
        print("Opted not to delete now.")
        

# Run main function
if __name__ == '__main__':
    wipe_from_file()


