
from preprocess import PreProcess
from scraper import Scraper
import os


def main():
    # init root path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    root_file_path = os.path.join(dir_path, '../data')

    # init data preprocess
    preprocess = PreProcess()
    preprocess.merge_tables(root_file_path)
    ids = preprocess.get_status_ids()

    # scrape tweets
    scraper = Scraper(ids)
    result = scraper.execute()


if __name__ == '__main__':
    main()
