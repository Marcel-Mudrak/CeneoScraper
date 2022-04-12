from encodings import utf_8
from tkinter.messagebox import NO
import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.ceneo.pl/95870086#tab=reviews'

all_opinions = []

while(url):
    response = requests.get(url)
    page_dom = BeautifulSoup(response.text, 'html.parser')
    opinions = page_dom.select('div.js_product-review')

    for opinion in opinions:

        opinion_id = opinion['data-entry-id']
        author = opinion.select_one('span.user-post__author-name').text.strip()

        try:
            rcmd = opinion.select_one('span.user-post__author-reccomendation > em').text.strip()
        except AttributeError:
            rcmd = None
            
        score = opinion.select_one('span.user-post__score-count').text.strip()
        content = opinion.select_one('div.user-post__text').text.strip()

        posted_on = opinion.select_one("span.user-post__published > time:nth-child(1)")['datetime'].strip()
        bought_on = opinion.select_one("span.user-post__published > time:nth-child(2)")['datetime'].strip()

        useful_for = opinion.select_one('button.vote-yes > span').text.strip()
        useless_for = opinion.select_one('button.vote-no > span').text.strip()

        pros = opinion.select('div.review-feature__title--positives ~ div.review-feature__item')
        cons = opinion.select('div.review-feature__title--negatives ~ div.review-feature__item')

        pros = [item.text.strip() for item in pros]
        cons = [item.text.strip() for item in cons]

        single_opinion = {
            'opinion_id': opinion_id,
            'author': author,
            'rcmd': rcmd,
            'score': score,
            'content': content,
            'posted_on': posted_on,
            'bought_on': bought_on,
            'useful_for': useful_for,
            'useless_for': useless_for,
            'pros': pros,
            'cons': cons
        }
        all_opinions.append(single_opinion)
        
    try:
        url = 'https://www.ceneo.pl' + page_dom.select_one('a.pagination__next')['href']
    except TypeError:
        url = None

print(json.dumps(all_opinions, indent=4, ensure_ascii=False))

with open('opinie.txt', 'w') as file:
    for opinion in all_opinions:
        for k, v in opinion.items():
            file.write(str(k) + ':\n' + str(v) + '\n\n')