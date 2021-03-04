#!/usr/bin/python3
# Prepares two json files of brief tweet data for deleting or keeping, based on arguments and favs


import tweepy
import keys
from datetime import datetime, timedelta
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
                 cache=None,
                 retry_count=3,
                 retry_delay=5,
                 retry_errors=set([401, 404, 500, 503]))


# little helper function, not used at the moment.
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
    #print(status.text)
   


def sort_timeline(date_start, date_end):
    account_name=keys.USER_NAME
    
    start_string = date_start.strftime("%m-%d-%Y")
    end_string = date_end.strftime("%m-%d-%Y")
    base_filename = "timeline-sort-"+ start_string + "_to_" + end_string
    
    keep_filename = "keep-" + base_filename + ".js"
    delete_filename = "delete-" + base_filename + ".js"

    keep_write = open(keep_filename, 'w')
    delete_write = open(delete_filename, 'w')
    
    keep_write.write("window.YTD.tweet.part0 = [")
    delete_write.write("window.YTD.tweet.part0 = [")
    
    first_tweet_keep = True
    first_tweet_delete = True


    for status in tweepy.Cursor(api.user_timeline, screen_name='@' + account_name).items():
        # Get the tweet id
        status_id = status._json['id']
        
       # Get whether you have favorited the tweet yourself
        status_favorited1 = status._json['favorited']

        # Get the datetime of the tweet
        status_date = datetime.strptime(status._json['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        print(status_date, 'Examining', status_id, ' favorited : ', status_favorited1)

        status_comp_date = parse(status._json['created_at'])      
           
        # If the difference between the current datetime and the tweet's
        # is more than the days threshold
        if (status_comp_date > date_start and status_comp_date < date_end):
            #inspect(status_id)
            tweet_min = {}
            tweet_min['id'] = status._json['id']
            tweet_min['created_at'] = status._json['created_at']
            tweet_min['full_text'] = status._json['text']
            # If you haven't favorited the tweet yourself
            if status_favorited1 == False:
                print("not favorited")
                if (first_tweet_delete == False):
                    delete_write.write(",")
                json.dump(tweet_min, delete_write, indent = 4, sort_keys=True)
            
                if (first_tweet_delete):
                    first_tweet_delete = False
                
            else:
                print("favorited")
                if (first_tweet_keep == False):
                    keep_write.write(",")
                json.dump(tweet_min, keep_write, indent = 4, sort_keys=True)
           
                if (first_tweet_keep):
                    first_tweet_keep = False

    keep_write.write("]")
    delete_write.write("]")

    keep_write.close()
    delete_write.close()

                 
# Run main function
if __name__ == '__main__':
    default_days_start = 60
    default_days_end = 90

    parser = OptionParser()
    parser.add_option("-a", "--days-start", dest="days_start",
                  help="start age in days to consider sorting timeline tweets.", metavar="DAYS_START")
    parser.add_option("-b", "--days-end", dest="days_end",
                  help="end age in days to consider sorting timeline tweets.", metavar="DAYS_END")
    parser.add_option("-s", "--date-start", dest="date_start",
                  help="Start date to consider sorting timeline tweets", metavar="DATE_START")
    parser.add_option("-e", "--date-end", dest="date_end",
                  help="End date to consider sorting timeline tweets", metavar="DATE_END")
        
    (options, args) = parser.parse_args()

    if ( (options.days_start and options.date_end) or (options.days_end and options.date_start)):
        #todo
        if (options.days_start and options.date_end):
            print('Cannot enter a date-end date and days-start var  -- choose one or the other.')
        if (options.days_end and options.date_start):
            print('Cannot enter a date-start date and days-end var  -- choose one or the other.')
    else:
    
        current_date = datetime.utcnow()
        # This will get overwritten if any command line arguments are used.
        #date_end = current_date - timedelta(days=default_days)

        # Validate dates
        if (options.date_start):
            date_start = utc.localize(parse(options.date_start))
        else:
            if (options.days_end):
                int_days = int(options.days_end)
                date_start = current_date - timedelta(days=int_days)
                date_start = utc.localize(date_start)
            else:
                date_start = current_date - timedelta(days=default_days_end)
                date_start = utc.localize(date_start)
            

        if (options.date_end):
            date_end = utc.localize(parse(options.date_end))
        else:
            if (options.days_start):
                int_days = int(options.days_start)
                date_end = current_date - timedelta(days=int_days)
                date_end = utc.localize(date_end)
            else:
                date_end = current_date - timedelta(days=default_days_start)
                date_end = utc.localize(date_end)
    
        if (date_end < date_start):
            print('you have selected start and end times that result in no overlap. Quitting.')
        else:
            sort_timeline(date_start, date_end)



