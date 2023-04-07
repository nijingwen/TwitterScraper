
from preprocess import PreProcess
from scraper import Scraper
import os
import boto3
import json
import os
import configparser


def main():
    # get config paser
    config = configparser.ConfigParser()

    # init root path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config.read(os.path.join(dir_path, '../config/data.config'))
    input_path = config['inputs']['filepath']
    root_path = os.path.join(dir_path, input_path)

    # init data preprocess
    preprocess = PreProcess()
    preprocess.merge_tables(root_path)
    ids = preprocess.get_status_ids()

    # scrape tweets
    scraper = Scraper(ids)
    result = scraper.execute(4)

    # write file to s3 bucket
    config.read(os.path.join(dir_path, '../config/s3.config'))
    bucket_name = config['s3_details']['bucket_name']
    filename = config['s3_details']['file_key']
    region = config['s3_details']['region']

    s3 = boto3.resource(
        's3',
        region_name=region
    )

    s3.Object(bucket_name, filename).put(
        Body=bytes(json.dumps(result).encode('UTF-8')))


if __name__ == '__main__':
    main()
