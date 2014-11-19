#!/usr/bin/python
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lyrics.settings")
from lyrics.models import Song
import csv

# set input file name here
INPUT = "collect_data/songs.csv"
MAX_BULK = 1000

if __name__=='__main__':
    csvfile = open(INPUT, 'rb')
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    bulk = []
    i = 0    
    for (aid, artist, title, duration, lyrics, url) in reader:
        if i<MAX_BULK:
            bulk.append(Song(aid=aid, artist=artist, title=title, duration=duration, url=url, lyrics=lyrics))
            i += 1

        else:
            Song.objects.bulk_create(bulk)
            bulk = []
            i = 0
        

