
from preprocess import PreProcess
from scraper import Scraper

def main():
    csv_file_paths = [
        '../data/twitter/2018/2018-01.csv', 
        '../data/twitter/2018/2018-02.csv'
    ]

    preprocess = PreProcess()
    preprocess.merge_tables(csv_file_paths)
    ids = preprocess.get_status_ids()

    scraper = Scraper(ids)
    scraper.execute()

if __name__ == '__main__':
    main()