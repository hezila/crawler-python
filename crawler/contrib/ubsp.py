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

import time, re
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

city_codes = {
    "new_york": 3
    }

BASE_URL = "http://www.urbanspoon.com/"

name_pattern = re.compile(r"(.*?)\([\d]+\)")
    
def chain_restaurants(city_name="new_york", proxies=None):
    city_code = city_codes[city_name]
    url = BASE_URL + "cities/%d/chains" % city_code

    html = get_response(url, proxies)
    if not html:
        logger.error('cannot fetch %s' % url)
        return
    soup = parse_soup(html)

    items = soup.find_all('li', {'class': 'bullet'})
    for item in items:
        restaurant = item.find('a')

        name = restaurant.string.encode('ascii', 'ignore')
        name_match = name_pattern.search(name)
        name = name_match.group(1)
        url = restaurant['href']
        yield name, url

def restaurants_of_chain(chain_url, proxies=None):
    html = get_response(chain_url, proxies)
    if not html:
        logger.error('cannot fetch %s' % chain_url)
        return
    soup = parse_soup(html)

    restaurant_list = soup.find_all('div', {'class': 'details'})
    for rst_item in restaurant_list:
        url = rst_item.find('a', {'class': 'resto_name'})['href']
        yield BASE_URL +  url
        
