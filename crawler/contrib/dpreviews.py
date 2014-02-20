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

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def dp_specs(spec_url, proxies=None):
    soup = get_soup(spec_url, proxies)

    specs_div = soup.find('div', {"class": "specificationsPage"})
    if specs_div is None:
        return None
    hds_items = specs_div.findAll('thead')
    specs_items = specs_div.findAll('tbody')

    techs = {}
    for i, item in enumerate(hds_items):
        inner_item = specs_items[i]
        key = ""
        if item.find('th'):
            key = item.find('th').getText()
            techs[key] = []
        else:
            continue

        for spec in inner_item.findAll('tr'):
            tech = {}
            if spec.find('th'):
                title = spec.find('th', {"class": "label"}).getText()
                value = unicode(spec.find('td', {"class": "value"})).encode('ascii', 'ignore')

                tech = (title, value)
                techs[key].append(tech)

    return techs