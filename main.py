from collections import Counter
from bs4 import BeautifulSoup
import json
import os
import requests
import re

#url = input('Адрес сайта: ')
#url = 'https://docs.djangoproject.com/en/4.1/topics/db/models/'
def parse_soup(url: str) -> str:
    """
    Функция считывания html страницы и вывода только текста страницы заключенного между тегами <body>
    :param url: str
    :return: str
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.find('body').text
# Проверяем существует ли файл
file_list = os.listdir()
if 'eng_dict.json' not in file_list:    # Если нет - создаем новый словарь (первый запуск программы)
    data = {'know': {}, 'dont_know': {}}
    print('Это первый запуск программы. Какую страничку будем разбирать?')
    url = input('Адрес сайта: ')
    body = str(parse_soup(url))
    word_list = re.findall(r'\b[a-zA-Z-]+\b', body)
    counter_dict = Counter(map(str.lower, word_list))
    print(f'Найдено слов: {len(counter_dict)}')
    for key, value in counter_dict.items():
        data['dont_know'][key] = value
else:
    with open('eng_dict.json', 'r', encoding='UTF-8') as file:  # Если есть - открываем его и работаем с ним
        data = json.load(file)

# Погнали по словам
print('Начнем разбирать слова, как только надоест набери EXIT')
key_for_del = []
for key, value in data['dont_know'].items():
    print(f'Ты знаешь слово {key}, оно встречается в тексте {value}')
    ask = input('+ (Да)/ - (Нет)')
    if ask.upper() == 'EXIT':
        break
    elif ask == '-':
        continue
    elif ask == '+':
        print('Как переводится это слово?:')
        translate = input().lower()
        data['know'][key] = (value, translate)
        key_for_del.append(key)
for el in key_for_del:
    del data['dont_know'][el]
print(f'Записей в словаре {len(data["dont_know"])}')
with open('eng_dict.json', 'w', encoding='UTF-8') as file:  # Сохраняем измененный словарь
    json.dump(data, file, ensure_ascii=False)