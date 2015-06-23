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
    a = dataset('data/test_positive', 'data/negative.csv')
    a.load()

if __name__ == '__main__':
  main()
