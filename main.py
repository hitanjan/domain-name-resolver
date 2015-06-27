#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Tool that spits out a domain for a company name with a high degree of accuracy.
"""

__author__ = 'hitanjan'


from input import dataset
import search
import util

def main():
    #result = search.get_data_order_by_page_rank("Segment",15, 11)
    #print result

    # csv_row = util.csv_reader("data/seed.csv").get_record()
    #
    # for i in csv_row:
    #     print(i)
    #
    a = dataset(positive_csv_data='data/positive.csv', negative_csv_data='data/negative.csv')
    data = a.load(build_cache=True)
    #
    # for key in data:
    #     print data[key].target_names
    #     print data[key].target
    #a = util.csv_dataset_creator("data/seed.csv", "data/positive.csv", "data/negative.csv")
    #a.create_files()


if __name__ == '__main__':
  main()
