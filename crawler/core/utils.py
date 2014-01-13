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

import os, sys, re

from lxml.html clean import clean_html
from lxml.html.soupparser import fromstring

import logging


logger = logging.getLogger('crawler.' + __name__)
logger.setLevel(logging.DEBUG)

def santitize_html(html):
    html = clean_html(html)
    return html

def remove_script(data):
    p = re.compile(r'<script .*?>.*?</script>')
    return p.sub(' ', data)

def remove_style(data):
    p = re.compile(r'<style .*?>.*?</style>')
    return p.sub(' ', data)

