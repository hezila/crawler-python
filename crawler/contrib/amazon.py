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

def amazon_prd_ids(search_url, proxies=None):
    logger.info('fetching product ids from %s' % search_url)
    soup = get_soup(search_url, proxies)

    prds_div = soup.findAll("div", {"class": "productTitle"})

    if not prds_div:
        prds_div = soup.findAll("div", {"class": "image imageContainer"})

    prds_ids = map(lambda x: x.find('a')['href'].split('/')[5], prds_div)


    for prd_id in prds_ids:
        yield prd_id

    time.sleep(5)

    pagnNextLink = soup.find("a", {"id": "pagnNextLink"})
    while pagnNextLink:
        next_link = pagnNextLink['href']
        logger.info('fetching product ids from %s' % next_link)
        
        soup = get_soup(next_link, proxies)
        prds_div = soup.findAll("div", {"class": "productTitle"})

        if not prds_div:
            prds_div = soup.findAll("div", {"class": "image imageContainer"})

        prds_ids = map(lambda x: x.find('a')['href'].split('/')[5], prds_div)
        
        for prd_id in prds_ids:
            yield prd_id

def amazon_camera(prd_id, proxies=None):
    brands = ['canon', 'sony', 'nikon', 'fuji', 'fujifilm', 'olympus',
              'oympus', 'panasonic', 'samsung', 'pentax', 'leica',
              'ricoh', 'casio', 'vivitar', 'benq', 'kodak', 'minox',
              'pen']

    prd_url = "http://www.amazon.com/dp/" + prd_id

    prd = {}
    prd['amazon_id'] = prd_id
    prd['amazon_url'] = prd_url

    logger.info('fetching the product info from %s' % prd_url)

    prd_soup = get_soup(prd_url, proxies)

    prd_title = prd_soup.find("h1", {"id": "title"}).text
    prd['amazon_raw_title'] = prd_title

    prd_title = prd_title.split()

    end = 0
    for index, item in enumerate(prd_title):
        if 'MP' == item:
            end = index
            break
        elif item.endswith('MP') and len(item) > 2:
            end = index + 1
            break

    size = len(prd_title)
    if end > 0:
        size = end + 1
    if prd_title[0].lower() in brands:
        if end > 0:
            prd_title = ' '.join(prd_title[:end-1])
        else:  prd_title = ' '.join(prd_title[:4])
    elif size > 1 and prd_title[1].lower() in brands:
        if end > 0:
            prd_title = ' '.join(prd_title[1:end-1])
        else: prd_title = ' '.join(prd_title[1:5])
    elif size > 2 and prd_title[2].lower() in brands:
        if end > 0:
            prd_title = ' '.join(prd_title[2:end-1])
        else: prd_title = ' '.join(prd_title[2:6])
    elif size > 3 and prd_title[3].lower() in brands:
        if end > 0:
            prd_title = ' '.join(prd_title[3:end-1])
    else:
        prd_title = '###' + ' '.join(prd_title)
        print prd_title

    if '/' in prd_title:
        index = prd_title.index('/')
        prd_title = prd_title[:index-1]

    prd['amazon_title'] = prd_title


    # TODO: fetch the technical details

    
    return prd

def amazon_prd_img(prd_id, target_dir=".", proxies=None):
    prd_url = "http://www.amazon.com/dp/" + prd_id
    logger.info("fetch picture from %s" % prd_url)
    prd_soup = get_soup(prd_url, proxies)

    img_container = prd_soup.find("div", {"id": "main-image-container"})

    img_container = img_container.find('div', {"id": "imgTagWrapperId"})

    image = img_container.find('img')

    data = get_response(image['src'], proxies)
    save = open(os.path.join(target_dir, prd_id) + '.jpg', 'wb')
    save.write(data)
    save.close()

def amazon_reviews(prd_id, proxies):
    prd_reviews = []
    base_review_url = "http://www.amazon.com/product-reviews/" + prd_id + "/?ie=UTF8&showViewpoints=0&pageNumber=" + "%s" + "&sortBy=bySubmissionDateDescending"

    pagn = "1"
    while True:
        prd_review_url = base_review_url % pagn
        logger.info('fetch reviews from %s' % prd_review_url)

        revs_html = get_response(prd_review_url, proxies)

        revs_soup = parse_soup(revs_html)

        reviews = extract_reviews(unicode(str(revs_html),
                                          errors="ignore"), prd_id)

        if reviews:
            prd_reviews.extend(reviews)

        pagn_bar = revs_soup.find("span", {"class": "paging"})
        pagn_bar_str = str(pagn_bar)

        mch = re.search(r"cm_cr_pr_top_link_next_([0-9]+)", pagn_bar_str)

        if mch is None:
            break
        if len(mch.groups()) > 0:
            pagn = mch.group(1)
            revs_soup.decompose()
        else:
            revs_soup.decompose()
            break
    return prd_reviews

def extract_reviews(data, pid):
    reviews = []
    #model_match = re.search(r'product\-reviews/([A-Z0-9]+)/ref\=cm_cr_pr', str)
    data = remove_extra_spaces(data)
    data = remove_script(data)
    data = remove_style(data)

    table_reg = re.compile(r"<table id=\"productReviews.*?>(.*)</table>")
    table_match = table_reg.search(data)
    if table_match:
        table_cont = table_match.group(1)
        review_reg = re.compile(r"-->(.*?)(!--|$)")
        review_matches = review_reg.findall(table_cont)
        if len(review_matches) > 0:
            # print "Review Number: ", len(review_matches)
            review_num = 0
            for index, review_match in enumerate(review_matches):
                review = {}
                block = review_match[0]

                end = review_match[1]

                help_reg = re.compile(
                    r"\> \<div.*?style=.*?\> ([\d]+) of ([\d]+) people found the following review helpful \<\/div\> \<")
                help_match = help_reg.search(block)
                if help_match:
                    # print "HELP: " + help_match.group(1) + " of " +
                    # help_match.group(2)
                    review["helpful_votes"] = int(help_match.group(1))
                    review["total_votes"] = int(help_match.group(2))

                block_reg = re.compile(
                    r"\<div.*?star_([1-5])_([05]).*?\<b\>(.*?)\<\/b\>.*?nobr\>(.*?)\<\/nobr")
                block_match = block_reg.search(block)
                if block_match:
                    review_num += 1
                    rating = block_match.group(1) + block_match.group(2)
                    # print "Rating:\t" + rating
                    review["overall_rating"] = float(rating)/10.0

                    title = block_match.group(3)
                    # print "Title:\t" + title
                    review["title"] = title

                    date = block_match.group(4)
                    date_reg = re.compile(r"([a-zA-Z]+) ([0-9]+), ([0-9]+)")
                    date_match = date_reg.search(date)
                    if date_match:
                        month = date_match.group(1)
                        if(month == "January"):
                            month = "01"
                        elif(month == "February"):
                            month = "02"
                        elif(month == "March"):
                            month = "03"
                        elif(month == "April"):
                            month = "04"
                        elif(month == "May"):
                            month = "05"
                        elif(month == "June"):
                            month = "06"
                        elif(month == "July"):
                            month = "07"
                        elif(month == "August"):
                            month = "08"
                        elif(month == "September"):
                            month = "09"
                        elif(month == "October"):
                            month = "10"
                        elif(month == "November"):
                            month = "11"
                        elif(month == "December"):
                            month = "12"
                        else:
                            month = "NULL"

                        new_date = month + " " + \
                            date_match.group(2) + ", " + date_match.group(3)
                        # print "Date:\t" + new_date
                        review["date"] = new_date

                        date_time = time.mktime(time.strptime(new_date, '%m %d, %Y'))
                        review['date_time'] = date_time

                        user_reg = re.compile(
                            r"\>By.*?\<\/div\>.*?\<a href=\"(.*?)\".*?\<span style =.*?\>(.*?)\<\/span\>\<\/a\>(.*?) - \<a href=\"(.*?)\"?\>See all my reviews\<\/a\>")
                        user_match = user_reg.search(block)

                        if user_match:
                            review["user"] = {}
                            # print "User:\t" + user_match.group(2)
                            review["user"]["name"] = user_match.group(2)
                            # print "User URL:\t" + user_match.group(1)
                            review["user"]["link"] = user_match.group(1)
                            # print "User Location:\t" + user_match.group(3)
                            review["user"]["location"] = user_match.group(3)
                            # print "User's Reviews:\t" + user_match.group(4)
                            review["user"]["others"] = user_match.group(4)

                            review["user_id"] = review["user"]["link"]
                        else:
                            #user_reg = re.compile(r"\>By.*?\<\/div\>.*?<a href=\"(.*?)\".*?\<span style = .*?\>(.*?)\<\/span\>\<\/a\>")
                            print "Oops 5 - Cannot match with user profile!"
                        purchase_reg = re.compile(
                            r"\<b class=.*?\>Amazon Verified Purchase\<\/b\>\<span")
                        purchase_match = purchase_reg.search(block)
                        if purchase_match:
                            # print "Purchased: " + "True"
                            review["purchased"] = 1
                        else:
                            review["purchased"] = 0

                        text = remove_cont_withtags(block)

                        

                        # print "Text:\t" + text
                        review["content"] = text.strip(' \t\n\r')
                        # print
                    else:
                        print "Oops 4: " + date

                else:
                    print "Oops 3: " + str(index)
                    
                print "Oops 3.0: " + str(index)
                print review

                review["product_id"] = pid

                if not "content" in review or len(review["content"]) == 0:
                    continue
                
                reviews.append(review)
        else:
            print "Oops2"
    else:
        print "Oops"

    return reviews


