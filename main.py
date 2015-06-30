#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Tool that spits out a domain for a company name with an accuracy of 80% or more.
"""

__author__ = 'hitanjan'


import engine
import search
import input
from optparse import OptionParser

def main():
    op = OptionParser()
    op.add_option("--predict",
              action="store", type="string", dest="query",
              help="Enter Company Name")

    (opts, args) = op.parse_args()
    if(opts.query):
        classifier = engine.load_classifier_template2()

        search_handle = search.bing()
        urls = search_handle.search(opts.query, limit=30)
        for url in urls:
            model = input.model(potential_url=url, company_name=opts.query)
            score = classifier.predict(model)
            if(score):
                print "Domain for Company Name - %s is %s" % (model.company_name, model.potential_url)
                break

        if(not score):
            print "Unable to predict domain for given Company Name - %s" % model.company_name



if __name__ == '__main__':
  main()
