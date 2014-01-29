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

from lxml.html.clean import clean_html
from lxml.html.soupparser import fromstring

import logging


logger = logging.getLogger('crawler.' + __name__)
logger.setLevel(logging.DEBUG)

def santitize_html(html):
    html = clean_html(html)
    return html

def remove_extra_spaces(data):
    p = re.compile(r'\s+')
    return p.sub(' ', data)


def remove_script(data):
    p = re.compile(r'<script .*?>.*?</script>')
    return p.sub(' ', data)

def remove_style(data):
    p = re.compile(r'<style .*?>.*?</style>')
    return p.sub(' ', data)

def remove_cont_withtags(data):
    style_reg = re.compile(r"\<style.*?\<\/style\>")
    data = style_reg.sub("", data)

    li_reg = re.compile(r"\<li.*?\<\/li\>")
    data = li_reg.sub("", data)

    table_reg = re.compile(r"\<table.*?\<\/table\>")
    data = table_reg.sub("", data)

    td_reg = re.compile(r"\<td.*?\<\/td\>")
    data = td_reg.sub("", data)
    
    div_reg = re.compile(r"\<div.*?\<\/div\>")
    data = div_reg.sub("", data)

    ul_reg = re.compile(r"\<ul.*?\<\/ul\>")
    data = ul_reg.sub("", data)

    a_reg = re.compile(r"\<a.*?\>.*?\<\/a\>")
    data = a_reg.sub("", data)


    data = re.sub(r"\<\/div\>", "", data)
    data = re.sub(r"\<div.*?\>.*?\<", "", data)
    data = re.sub(r"\<\/table\>", "", data)
    data = re.sub(r"\<\/td\>", "", data)
    data = re.sub(r"\<\/tr\>", "", data)

    data = re.sub(r"\<br \/\>", "\n", data)
    data = re.sub(r"[\s]+?\<", " ", data)
    data = re.sub(r"\n+", "\n", data)
    return data
