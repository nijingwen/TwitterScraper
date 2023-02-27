import json
from snscrape.modules.twitter import TwitterTweetScraper, TwitterTweetScraperMode
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import multiprocessing

class Scraper:
    def __init__(self, tweet_ids: list) -> None:
        self.tweet_ids = tweet_ids

    # scrape data
    def _get_specific_tweet(self, tweet_id):
        for i,tweet in enumerate(TwitterTweetScraper(tweetId=tweet_id, mode=TwitterTweetScraperMode.SINGLE).get_items()):
            # ?? just one tweet?
            return json.loads(tweet.json())
    
    # multithreading strategy
    def _execute_with_multithreads(self, i: int, j: int):
        results = None
        # implement multithreading
        with ThreadPoolExecutor() as executor:
            results = executor.map(self._get_specific_tweet, self.tweet_ids[i:j])
        return list(results)
    
    def execute(self, chunk_size: int=1000):
        with ProcessPoolExecutor(multiprocessing.cpu_count()) as executor:
            results = list()

            for i in range(0, len(self.tweet_ids), chunk_size):
                j = i + chunk_size if i + chunk_size < len(self.tweet_ids) else len(self.tweet_ids)
                results.append(executor.submit(self._execute_with_multithreads, i, j))
            
        # a_tweet = pd.DataFrame([tweet]) 
        # if tweet is None:
        #     unable_to_get.append(id)
        # else:   
        #     tweets = pd.concat([tweets, a_tweet])
