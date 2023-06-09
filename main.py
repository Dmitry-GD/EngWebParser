from art import tprint
from collections import Counter
from bs4 import BeautifulSoup
import json
import os
import requests
import re

def parse_soup(url: str) -> str:
    """
    Функция считывания html страницы и вывода только текста страницы заключенного между тегами <body>
    :param url: str
    :return: str
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.find('body').text

def search_in_dict(word: str) -> str:
    """
    Поиск слова во внешнем словаре
    :param word: str
    :return: str
    """
    for el in dictionary_eng_ru:
        if word in el['en']:
            return el['ru']
        else:
            return 'НЕ НАЙДЕНО'

def my_stat():
    """
    Вывод статистики
    :return: None
    """
    print('*************************************************')
    print(f'* Записей в словаре: {len(data["know"]) + len(data["dont_know"])}')
    print(f'* Из них известных слов: {len(data["know"])}')
    print(f'* Из них слов которые надо выучить: {len(data["dont_know"])}')
    print('*************************************************')

def guess_words():
    """
    Перебираем слова в словаре data
    :return: None
    """
    print('Начнем разбирать слова, как только надоест набери EXIT')
    key_for_del = []
    for key, value in data['dont_know'].items():
        print(f'Ты знаешь слово "{key}"? Оно встречается в тексте {value} раз.')
        print('+ (Да)/ - (Нет)/ EXIT для выхода')
        ask = input()
        if ask.upper() == 'EXIT':
            break
        elif ask == '-':
            translate = search_in_dict(key)
            if translate != 'НЕ НАЙДЕНО':
                print(f'Это слово переводится как: "{translate}"')
            else:
                print(f'В нашей версии словаря это слово {translate}')
            continue
        elif ask == '+':
            print('Как переводится это слово?:')
            translate = input().lower()
            data['know'][key] = (value, translate)
            key_for_del.append(key)
    for el in key_for_del:
        del data['dont_know'][el]
    print()

def parse_and_add_words():
    """
    Парсим html страницу и добавляем новые слова в существующй словарь data
    :return: None
    """
    url = input('Адрес сайта: ')
    body = str(parse_soup(url))
    word_list = re.findall(r'\b[a-zA-Z-]+\b', body)
    counter_dict = Counter(map(str.lower, word_list))
    print(f'Найдено слов: {len(counter_dict)}')
    data['count_page'] += 1
    data['list_page'].append(url)
    for key, value in counter_dict.items():
        if key not in data['know'].keys():
            if key not in data['dont_know'].keys():
                data['dont_know'][key] = value
            else:
                data['dont_know'][key] = data['dont_know'].get(key) + value
        else:
            data['know'][key][0] = data['know'][key][0] + value

# Загружаем внешний англо-русский словарь
with open('words.json', 'r', encoding='UTF-8') as dict_file:
    dictionary_eng_ru = json.load(dict_file)

# Приветствие
tprint("Tech   ENG   for   Me")
print(f'### Привет! Сегодня будем парсить странички и учить новые неизвестные слова ###')

# Проверяем существует ли файл
file_list = os.listdir()
if 'eng_dict.json' not in file_list:    # Если нет - создаем новый словарь (первый запуск программы)
    data = {'know': {}, 'dont_know': {}, 'count_page': 0, 'list_page': []}
    print('Это первый запуск программы. Какую страничку будем разбирать?')
    parse_and_add_words()
else:
    with open('eng_dict.json', 'r', encoding='UTF-8') as file:  # Если есть - открываем его и работаем с ним
        data = json.load(file)

# Начало
while True:
    print()
    print('Выбери действие:\n1 - загрузить новые слова\n2 - разобрать те слова, что уже есть\n3 - вывести статистику\n4 - выйти')
    user_select = input('Твой выбор: ')
    if user_select == '1':
        parse_and_add_words()
    elif user_select == '2':
        guess_words()
    elif user_select == '3':
        my_stat()
    elif user_select == '4':
        break
    else:
        print('Вводи корректные значения, пожалуйста!')

# Сохраняем измененный словарь при выходе
with open('eng_dict.json', 'w', encoding='UTF-8') as file:
    json.dump(data, file, ensure_ascii=False)

'''
Добавить предупреждение, когда словарь с неразобранными словами заканчивается
Добавить статистику по весу слов
'''