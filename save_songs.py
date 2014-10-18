#!/usr/bin/python
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lyrics.settings")
from lyrics.models import Song
import csv

# set input file name here
INPUT = "collect_data/songs.csv"


if __name__=='__main__':
    csvfile = open(INPUT, 'rb')
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for (aid, artist, title, duration, url, lyrics) in reader:
        s = Song(aid=aid, artist=artist, title=title, duration=duration, url=url, lyrics=lyrics)
        s.save()
        

