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

from crawler.contrib.dpreviews import *

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

    

    techs = dp_specs("http://www.dpreview.com/products/panasonic/compacts/panasonic_dmcsz3/specifications")
    print "<table>"
    for k in techs.keys():
        print "<thead><tr><th>%s<th></tr></thead>" % k
        print "<tbody>"
        for key, value in techs[k]:
            print '<tr><td>%s</td><td>%s</td></tr>' % (key, value)
        print "</tbody>"
    # for k in techs:
    #     print '<tr><td>%s</td><td>%s</td></tr>' % (k, techs[k].encode('ascii', "ignore"))
    print "</table>"
    # for dirname, dirnames, filenames in os.walk('D:\workspace\camera\small'):
    #     for filename in filenames:
    #         file_path = os.path.join(dirname, filename)
            
    #         pid = filename[:-5]
    #         if not os.path.isfile(os.path.join("D:\workspace\camera\images", pid) + ".jpg"):
    #             amazon_prd_img(pid, "D:\workspace\camera\images")

    #         print pid
   
if __name__ == "__main__":
    main()
