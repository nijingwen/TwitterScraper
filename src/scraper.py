import json
from snscrape.modules.twitter import TwitterTweetScraper, TwitterTweetScraperMode
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed, Future
import multiprocessing
import math


class Scraper:
    def __init__(self, tweet_ids: list) -> None:
        self.tweet_ids = tweet_ids

    # set error message
    def _set_error(self, tweet_id: str, message: str) -> str:
        return json.dumps({
            'error': message,
            'id': tweet_id
        })

    # get future result ignoring error
    def _try_read_future_result(self, future: Future):
        try:
            return future.result()
        except:
            return json.loads(self._set_error('unknown_id', str(future.exception())))

    # scrape data
    def _get_tweet(self, tweet_id: str):
        try:
            for i, tweet in enumerate(TwitterTweetScraper(tweetId=tweet_id, mode=TwitterTweetScraperMode.SINGLE).get_items()):
                return json.loads(tweet.json()) if type(tweet.json()) is str else json.loads(self._set_error(tweet_id, 'tweet json() did not return in str'))
        except Exception as err:
            return json.loads(self._set_error(tweet_id, str(err)))

    # multithreading strategy
    def _execute_with_multithreads(self, start: int, end: int) -> list:
        futures = None
        # implement multithreading
        with ThreadPoolExecutor() as executor:
            futures = executor.map(
                self._get_tweet, self.tweet_ids[start:end])

        return [future for future in futures if future]

    def _execute_with_multiprocessors(self, cpu_count: int) -> list:
        chunk_size = math.ceil(len(self.tweet_ids) / cpu_count)
        futures = list()
        with ProcessPoolExecutor(cpu_count) as executor:
            for i in range(cpu_count):
                start, end = i * chunk_size, (i + 1) * chunk_size
                if i == cpu_count - 1:
                    end = len(self.tweet_ids)

                futures.append(executor.submit(
                    self._execute_with_multithreads, start, end))

        return [result for future in as_completed(futures) for result in self._try_read_future_result(future)]

    def execute(self, cpu_count: int = multiprocessing.cpu_count()):
        return self._execute_with_multiprocessors(cpu_count)
