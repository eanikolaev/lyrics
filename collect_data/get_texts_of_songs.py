#-*- coding: utf-8 -*-
"""
    get texts of songs using VK API

    1) search text of songs by id: https://vk.com/dev/audio.getLyrics
    2) try to apply language model
    3) if song is russian (>=50% rus words) and contains enough words (>=10) - save text into csv-file

    csv: id_of_song | flag | text
    flag: russian / not_russian / not_processed / not_enough

    not_enough : amount of words < 10
"""

import requests
import datetime, time
import csv
import argparse
import os

# set your token and id here
TOKEN  = "0aeefbf4704243845df36ac67f25c587f23e48cd9a4f23c8aeab97561c43cf2de4802ca7dbec629743252"
FILE_WITH_TEXTS = "texts_of_songs.csv"

from pymorphy import get_morph  # Морфологический анализатор https://pythonhosted.org/pymorphy/intro.html
morph = get_morph('/home/antre/pymorphy_dicts/')    # Директория со словарями для pymorphy
RUS_LETTERS = "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ".decode('utf-8')
ENG_LETTERS = "QWERTYUIOPASDFGHJKLZXCVBNM'".decode('utf-8')

russian_words = set()

print "Normalize Tolstoj tokens..."
csvfile0 = open('tokens_from_tolstoj.csv', 'rb')
reader0 = csv.reader(csvfile0, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
for e in reader0:
    for term in morph.normalize(e[0].decode('utf-8').upper()):
        russian_words.add(term)
csvfile0.close()
print "Normalized"


def parse_data(s):
    """
    Парсинг текста песни и пословное сопоставление со словарем
    Возвращает число слов языка и число слов в песне

    """
    word = ""
    word_started = False

    count = 0
    intersect = 0

    for sign in s:
        if word_started:
            if sign in (RUS_LETTERS + ENG_LETTERS + '-'.decode('utf-8')):
                # Слово продолжается
                word += sign
            else:
                # Слово закончилось
                set_of_normalized = morph.normalize(word)
                if type(set_of_normalized).__name__ == 'set' and set_of_normalized & russian_words:
                    intersect += 1
                count += 1
                word_started = False
        else:
            if sign in RUS_LETTERS + ENG_LETTERS:
                # Слово началось
                word = sign
                word_started = True

    if word_started and word != "":
        set_of_normalized = morph.normalize(word)
        if type(set_of_normalized).__name__ == 'set' and set_of_normalized & russian_words:
            intersect += 1
        count += 1
    return intersect, count


class Api(object):

    endpoint = ''

    def __init__(self, access_token):
        self.access_token = access_token

    def call(self, method, **params):
        request_params = params.copy()
        request_params["access_token"] = self.access_token
        try:
            response = requests.get(self.endpoint.format(method=method), params=request_params)
            if response.status_code != 200:
                raise requests.exceptions.RequestException("Bad status code {}".format(response.status_code))
            return response.json()
        except requests.exceptions.RequestException as re:
            print "A n API call failed with exception {}".format(re)
            raise


class VkApi(Api):
    endpoint = "https://api.vk.com/method/{method}"

    def search_songs(self, query):
        time.sleep(0.21)
        try:
            json = self.call("audio.getLyrics", lyrics_id=query)        # [, param=value]
            return json.get("response", "").get("text", "")
        except (AttributeError, requests.ConnectionError):
            return ""


def parse_args():
    """
    Парсинг аргументов командной строки
    """
    c_l_parser = argparse.ArgumentParser(description='Сбор текстов песен')
    c_l_parser.add_argument('-n', dest='songs_to_analyze', type=int, default=1000, help='Файл с текстами песен')
    return c_l_parser.parse_args()


def main():    
    api = VkApi(TOKEN)

    args = parse_args()
    songs_left_to_patse = args.songs_to_analyze

    csvfile = open(FILE_WITH_TEXTS, 'rb')
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    csvfile2 = open('temptemptemp.csv', 'wb')
    writer = csv.writer(csvfile2, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for row in reader:
        if len(row) == 1:
            text_id, flag, text = row[0], 'not_processed', ''
        elif len(row) == 2:
            text_id, flag, text = row[0], row[1], ''
        elif len(row) > 2:
            text_id, flag, text = row[0], row[1], row[2]
        else:
            print "Unexpected error"
            return

        if flag == 'not_processed' and songs_left_to_patse > 0:
            text = api.search_songs(text_id)

            # Detect language
            intersect, count = parse_data(text.upper())
            if count == 0:
                flag = 'not_processed'
            elif count < 10:
                songs_left_to_patse -= 1
                flag = 'not_enough'
            else:
                songs_left_to_patse -= 1
                if intersect*1.0/count >= 0.5:
                    flag = 'russian'
                else:
                    flag = 'not_russian'

            print text_id, ":", intersect, "/", count, flag
            text = text.encode("utf-8")

        writer.writerow([text_id, flag, text])
    csvfile.close()
    csvfile2.close()

    for filename in os.listdir("."):
        if filename.startswith("temptemptemp"):
            os.rename(filename, FILE_WITH_TEXTS)


if __name__ == "__main__":
    main()
