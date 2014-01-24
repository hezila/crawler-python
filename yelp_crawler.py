#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Copyright (c) 2014 Feng Wang <wffrank1987@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
'''

from crawler.contrib.yelp import *

from optparse import OptionParser

import time
import pprint
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


usage = "usage %prog [options] arg"
parser = OptionParser(usage=usage)
parser.add_option('-c', "--category", dest="category",
                  help="the target bussiness category")
parser.add_option("-l", "--location", dest="location",
              help="the target location/country")
parser.add_option("-o", "--output", dest="output_dir",
              help="write out to DIR")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
parser.add_option("-q", "--quiet", action="store_false", dest="verbose")

(options, args) = parser.parse_args()

def main():
    """
    Warnining: your ip would be banned by yelp if you don't use proxy

    goagent proxy: https://code.google.com/p/goagent/
    http://www.hidemyass.com/proxy-list/

    """


    proxies = {'http': 'http://23.244.180.162:8089', 'https': 'http://23.244.180.162:8089'}
    #proxies = {'http': 'socks5://71.235.242.33:38626'}
    #yelp_biz_ids("restaurants", "new+york", proxies)
    
    for biz_url in yelp_biz_ids("restaurants", "New+York", proxies):
        biz = yelp_biz(biz_url, proxies)
        pprint.pprint(biz)

if __name__ == "__main__":
    main()
