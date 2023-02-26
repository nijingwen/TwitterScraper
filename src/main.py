
from preprocess import PreProcess
from scraper import Scraper

def main():
    # init root path
    root_file_path = '../data'

    # init data preprocess
    preprocess = PreProcess()
    preprocess.merge_tables(root_file_path)
    ids = preprocess.get_status_ids()

    # scrape tweets
    scraper = Scraper(ids)
    scraper.execute()

if __name__ == '__main__':
    main()