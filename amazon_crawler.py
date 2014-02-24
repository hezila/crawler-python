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

from crawler.contrib.amazon import *

from optparse import OptionParser
import os
import time
import pprint
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


usage = "usage %prog [options] arg"
parser = OptionParser(usage=usage)
parser.add_option('-s', "--seed", dest="initial search url",
                  help="the initial search url")
parser.add_option("-o", "--output", dest="output_dir",
              help="write out to DIR")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
parser.add_option("-q", "--quiet", action="store_false", dest="verbose")

(options, args) = parser.parse_args()

def main():

    proxies = {'http': 'http://23.244.180.162:8089', 'https': 'http://23.244.180.162:8089'}

    socket_proxies = {'http': 'socket5://1.ss.shadowsocks.net:65535', 'https': 'http://23.244.180.162:8089'}

    # laptop seed url
    #seed_url = "http://www.amazon.com/s/ref=sr_nr_p_n_feature_eighteen_0?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A565108%2Cp_n_feature_eighteen_browse-bin%3A6819965011&bbn=565108&ie=UTF8&qid=1381818929&rnid=6819964011"
    
    #for prd_id in amazon_prd_ids(seed_url, proxies):
    #    print prd_id

    #print amazon_camera("B00EFILPHA", proxies)

    print amazon_reviews("B00EFILPHA")
    # amazon_prd_img("B00EFILPHA", "images")

    #for dirname, dirnames, filenames in os.walk('D:\workspace\camera\small'):
    #    for filename in filenames:
    #        file_path = os.path.join(dirname, filename)
            
    #        pid = filename[:-5]
    #        if not os.path.isfile(os.path.join("D:\workspace\camera\images", pid) + ".jpg"):
    #            amazon_prd_img(pid, "D:\workspace\camera\images")

     #       print pid
   
if __name__ == "__main__":
    main()
