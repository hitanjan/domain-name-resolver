#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Tool that spits out a domain for a company name with a high degree of accuracy.
"""

__author__ = 'hitanjan'

import pprint
import json
import sys
from googleapiclient.discovery import build
from input import dataset


def main():
    a = dataset(positive_csv_data='data/test_positive', negative_csv_data='data/test_negative')
    data = a.load(build_cache=True)
    for key in data:
        print data[key].target_names
        print data[key].target

if __name__ == '__main__':
  main()
