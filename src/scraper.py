import json
import pandas as pd
from snscrape.modules.twitter import TwitterTweetScraper, TwitterTweetScraperMode

class Scraper:
    def __init__(self, tweet_ids: list) -> None:
        self.tweet_ids = tweet_ids

    # scrape data
    def _get_specific_tweet(self, tweet_id):
        for i,tweet in enumerate(TwitterTweetScraper(tweetId=tweet_id,mode=TwitterTweetScraperMode.SINGLE).get_items()):
            # print(tweet)
            return json.loads(tweet.json())
    
    def execute(self):
        # scrape data and store in pandas dataframe
        for id in self.tweet_ids:
            tweet = self._get_specific_tweet(id)
            print(tweet)

            # a_tweet = pd.DataFrame([tweet]) 
            # if tweet is None:
            #     unable_to_get.append(id)
            # else:   
            #     tweets = pd.concat([tweets, a_tweet])
        
        # print(tweets)
