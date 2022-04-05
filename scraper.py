import requests
from bs4 import BeautifulSoup

url = 'https://www.ceneo.pl/45863470#tab=reviews'

response = requests.get(url)

page_dom = BeautifulSoup(response.text, 'html.parser')

opinions = page_dom.select('div.js_product-review')
opinion = opinions.pop(3)

opinion_id = opinion['data-entry-id']
author = opinion.select_one('span.user-post__author-name').text.strip()
rcmd = opinion.select_one('span.user-post__author-reccomendation > em').text.strip()
score = opinion.select_one('span.user-post__score-count').text.strip()
content = opinion.select_one('div.user-post__text').text.strip()

posted_on = opinion.select_one("span.user-post_published > time:nth-child(1)'\['datetime\]").text.strip()
bought_on = opinion.select_one("span.user-post_published > time:nth-child(2)'\['datetime\]").text.strip()

useful_for = opinion.select_one('button.vote-yes > span').text.strip()
useless_for = opinion.select_one('button.vote-no > span').text.strip()

pros = opinion.select_one('div.review-feature__title--positives ~ div.review-feature__item').text.strip()
cons = opinion.select_one('div.review-feature__title--negatives ~ div.review-feature__item').text.strip()

pros = [item.text.strip() for item in pros]
cons = [item.text.strip() for item in cons]

print(type(pros))
print(pros)


# with open('opinie.html', 'w') as file:
# 	file.write(opinion.prettify())

# print(opinion.prettify())