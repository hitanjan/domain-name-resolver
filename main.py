#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tool that spits out a domain for a company name with a high degree of accuracy.
"""

__author__ = 'hitanjan'

import pprint
import json
import sys
from googleapiclient.discovery import build


def main():
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",
            developerKey="AIzaSyCQkiO-7Rj4fnFRRYViGPluyJzxnd6hQCE")

  res = service.cse().list(
      q=sys.argv[1],
      num=1,
      cx='000176173689670368806:urydus__up0',
    ).execute()
  #pprint.pprint(res)
  print 'URL: %s' % res['items'][0]['link']

if __name__ == '__main__':
  main()
