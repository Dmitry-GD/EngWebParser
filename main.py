from collections import Counter
from bs4 import BeautifulSoup
import requests
import re

#url = input('Адрес сайта: ')
url = 'https://docs.djangoproject.com/en/4.1/topics/db/models/'
def parse_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.find('body').text
body = str(parse_soup(url))
word_list = re.findall(r'\b[a-zA-Z-]+\b', body)
word_list = list(map(str.lower, word_list))
counter_dict = Counter(word_list)
print(counter_dict)
print('>>>>>>>>>>>>>')
print(f'Найдено слов: {len(counter_dict)}')