# This code is largely copied from the code written by Joe Gregorio
# Original code may be found here - https://github.com/google/google-api-python-client/tree/master/samples/customsearch

import pprint
import json
import sys
from googleapiclient.discovery import build


__auth__ = "AIzaSyCQkiO-7Rj4fnFRRYViGPluyJzxnd6hQCE"
__cse_id__ = '000176173689670368806:gp5yn6rybga'


def get_data(search_key, num_results=20):
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.

    #print num_results
    service = build("customsearch", "v1",
                    developerKey=__auth__)

    cse = service.cse()

    it = [(int(b*10 +1),10) for b in range(num_results/10)]
    it += [((num_results/10)*10 +1, num_results%10)] if num_results%10!=0 else []


    #print it

    url_list = [cse.list(q=search_key,
                   cx=__cse_id__,
                   start = a,
                   num = b
                   ).execute()['items'][c]['link'] for (a,b) in it for c in range(b)]

    return url_list
