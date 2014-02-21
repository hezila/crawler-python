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

from crawler.core.base import *

import time
import logging

try:
    import simplejson as json
except Exception, e:
    import json

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

base_url = 'http://www.engadget.com/'

def gdgt_prds(category_id, proxies=None):
    """
    category_id : 2 for camera
    36 for laptop
    """
    url = base_url + 'a/category_filter/?category_id=%d&sort=score&offset=%d'
    offset = 0
    while True:
        print 'begin with %d ...' % offset
        search_url = url % (category_id, offset)
        #print 'fetching %s' % search_url
        html = get_response(search_url, proxies)
        json_doc = json.loads(html)

        if json_doc['success']:
            for prd in json_doc['products']:
                if prd['availability'] == 1:
                    yield prd 
                # pid = prd['product_id']
                # json_file = open(os.path.join('engadget_prd', pid), 'w')
                # json_file.write(
                #     json.dumps(prd, sort_keys=True, indent=4, separators=(',', ': ')))
                # json_file.close()
        else:
            break
        offset += 40

def _get_amazon_product(gdgt_url):
    """ Check the relevant amazon url

    @param gdgt_url - the gdgt product url
    """
    soup = get_soup(gdgt_url)
    price_compare_divs = soup.findAll(
        'div', {'class': 'price-comparison-retailer'})
    if price_compare_divs:
        print 'HAS COMPARE'
        for div in price_compare_divs:
            link = div.find('a')
            if link:
                if link.find('img') and link.find('img')['alt'] == 'Amazon.com':
                    print link['href']
                    return _get_amazon_pid(link['href'])
    else:
        print 'WARNING: None amazon related'
    print None


def _get_amazon_pid(url):
    #header = get_header(mech, url)
    soup = get_soup(url)
    amazon_url = soup.head.find('link', {'rel': 'canonical'})['href']
    amazon_pid = amazon_url.split('/')[-1]
    return (amazon_url, amazon_pid)

def get_amazon_ids(logfile):
    logs = open(logfile, 'r')
    

    outamazon = open('outamazon.txt', 'w')

    for line in logs:
        pid, name, url, picture = line.strip().split('\t')
        item = _get_amazon_product(url)
        if item is None:
            continue
        amz_url, amz_pid = item
        if amz_url is not None:
            outamazon.write("%s\t%s\t%s\t%s\t%s\n" % (amz_pid, name, amz_url, url, picture))
            outamazon.flush()
    outamazon.close()

