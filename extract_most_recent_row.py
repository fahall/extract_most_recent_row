import argparse
import csv
import logging
import re
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data(input_file):
    logger.info('Reading input file: ' + input_file)
    with open(input_file, 'r') as f:
        r = csv.reader(f)
        data = [row for row in r]
    return data


def get_date_col_idx(header):
    return header.index('date')


def get_row_date(row, date_idx):
    string = row[date_idx]
    parts = re.findall(r"[\w']+", string)
    date_string = ' '.join([s[-2:] for s in parts])
    return datetime.strptime(date_string, '%m %d %y')


def get_most_recent_row(rows):
    header = rows[0]
    date_idx = get_date_col_idx(header)
    logger.info('Checking dates')
    all_dates = [get_row_date(r, date_idx) for r in rows[1:]]
    max_date_idx = all_dates.index(
        max(all_dates)) + 1  # skipped header, so add 1
    return rows[max_date_idx]


def save_most_recent_row(row, output):
    logger.info('Saving most recent row to: ' + output)
    with open(output, 'w') as f:
        writer = csv.writer(f)
        writer.writerows([row])


def main(input_file, output_file):
    data = load_data(input_file)
    most_recent_row = get_most_recent_row(data)
    save_most_recent_row(most_recent_row, output_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract most recent row from csv and put into another csv')
    parser.add_argument('-i', '--input', help='Input File', required=True)
    parser.add_argument(
        '-o', '--output', help='Output file to store result (WILL OVERWRITE)', required=True)
    args = vars(parser.parse_args())
    main(args['input'], args['output'])
