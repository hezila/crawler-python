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

logger = logging.getLogger('crawler.' + __name__)
logger.setLevel(logging.DEBUG)

def yelp_biz_ids(cate, loc, proxies=None):
    start = 0
    step = 10
    while True:
        url = "http://www.yelp.com/search?cflt=%s&start=%d&find_loc=%s" % (cate, start, loc)

        logger.info('fetching from %s' % url)

        html = get_response(url, proxies)
        soup = parse_soup(html)
        
        bussiness_divs = soup.findAll('div', {'class': "search-result natural-search-result biz-listing-large"})
        for div in bussiness_divs:
            bussiness_story = div.find('div', {'class': "media-story"})
            title_div = bussiness_story.find('h3', {"class": "search-result-title"}).find('a')
            url = 'http://www.yelp.com%s' % title_div['href']
            #title = title_div.text
            #print '%s -> %s' % (title, url)
            yield url
        start += step
        time.sleep(5)

def yelp_biz(biz_url, proxies=None):
    biz = {}
    biz['url'] = biz_url

    biz_url = '%s?nb=1' % biz_url # the argument 'nb=1' is required

    logger.info('fetching %s' % biz_url)

    soup = get_soup(biz_url, proxies)

    top_self_div = soup.find('div', {'class': "top-shelf"})

    title_div = top_self_div.find('h1', {'itemprop': "name"})
    title = title_div.text
    biz['title'] = title

    rating_div = top_self_div.find(
        'div', {'class': "rating-info clearfix"})
    review_span = rating_div.find('span', {"itemprop": "reviewCount"})
    review_count = int(review_span.text)
    biz['review_num'] = review_count

    price_category_div = top_self_div.find(
        'div', {'class': "price-category"})
    price_range = price_category_div.find(
        'span', {"class": "business-attribute price-range"})
    if price_range:
        biz['price_range'] = len(price_range.text.strip())

    categories = map(lambda x: (x.text, 'http://www.yelp.com%s' %
                     x['href']), price_category_div.findAll('a'))
    biz['categories'] = categories

    map_div = top_self_div.find('div', {"class": "mapbox-text"})
    address_div = map_div.find('li', {"class": "address"})
    address = {}
    for span in address_div.findAll('span'):
        if 'itemprop' not in span:
            continue
        key = span['itemprop']
        value = span.text
        address[key] = value
    biz['address'] = address

    action_url = soup.find('ul', {'class': 'action-link-list'}).find('a')['href']

    biz_id = action_url.split('&')[0].split('=')[-1]
    
    biz['id'] = biz_id

    
    biz["longitude"] = soup.head.find("meta", {"property": "place:location:longitude"})["content"]
    biz["latitude"] = soup.head.find("meta", {"property": "place:location:latitude"})["content"]


    # reviews
    reviews_page_div = soup.find('div', {'class': "page-of-pages"})
    pages = int(reviews_page_div.text.split()[-1])

    reviews_div = soup.find('div', {'class': "review-container"})
    reviews = reviews_in_page(reviews_div)

    for page in xrange(1, pages + 1):
        start = page * 40
        rurl = '%s&start=%d' % (biz_url, start)
        
        page = get_soup(rurl, proxies).find('div', {'class': "review-container"})
        for r in reviews_in_page(page):
            reviews.append(r)
    biz['reviews'] = reviews

    return biz

def reviews_in_page(soup):
    reviews = []

    for review_div in soup.findAll("li", {'class': 'review'}):
        review = {}

        passport_info_ul = review_div.find(
            'ul', {'class': 'user-passport-info'})
        author = {}
        if passport_info_ul:
            author_name_li = passport_info_ul.find(
                'li', {'class': 'user-name'}).find('a')
            if not author_name_li:
                continue
            name = author_name_li.text
            author_url = author_name_li['href']
            author_id = author_url.split('=')[-1]
            author_url = 'http://www.yelp.com%s' % author_url
            author['name'] = name
            author['id'] = author_id
            author['url'] = author_url

        author_location_li = passport_info_ul.find(
            'li', {'class': 'user-location'})
        if author_location_li:
            author['location'] = author_location_li.text
        review['author'] = author

        review_content_div = review_div.find(
            'div', {'class': 'review-content'})
        rating = float(review_content_div.find(
            "meta", itemprop="ratingValue")["content"])
        review['rating'] = rating

        date = review_content_div.find(
            'meta', itemprop='datePublished')['content']
        review['date'] = date

        checkin_div = review_div.find(
            'span', {'class': 'i-wrap ig-wrap-common i-checkin-burst-blue-small-common-wrap badge checkin checkin-irregular'})
        if checkin_div:
            checkin = int(checkin_div.text.strip().split()[0])
            review['checkin'] = checkin

        text_div = review_div.find(
            'p', {'class': 'review_comment ieSucks'})
        
        if not text_div:
            continue

        ps = []

        brs = text_div.findAll('br')
        if not brs:
            ps.append(text_div.text.encode('ascii', 'ignore'))
        else:
            for i, br in enumerate(text_div.findAll('br')):
                if i == 0:
                    prev = br.previousSibling
                    if not(prev and isinstance(prev, NavigableString)):
                        continue
                    ps.append(prev.strip().encode('ascii', 'ignore'))

                next = br.nextSibling
                
                if not (next and isinstance(next,NavigableString)):
                    continue
                ps.append(next.strip().encode('ascii', 'ignore'))

        review['content'] = '\n'.join(ps)

        useful_div = review_div.find("li", class_="useful ufc-btn")
        if useful_div:
            useful = useful_div.find(
                "span", recursive=False).text
            review['useful'] = useful

        funny_div = review_div.find("li", class_="funny ufc-btn")
        if funny_div:
            funny = funny_div.find(
                "span", recursive=False).text
            review['funny'] = funny

        cool_div = review_div.find("li", class_="cool ufc-btn")
        if cool_div:
            cool = cool_div.find(
                "span", recursive=False).text
            review['cool'] = cool

        reviews.append(review)
    return reviews
