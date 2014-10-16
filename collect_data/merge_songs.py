"""
    merge two songs.csv files in one
"""

import csv

# set input1, input2 and output filenames here
INPUT1 = "songs1.csv"
INPUT2 = "songs2.csv"
OUTPUT = "songs_merged.csv"


if __name__=='__main__':
    csvfile = open(INPUT1, 'rb')
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    all_songs = {}
    for row in reader:
        if not all_songs.has_key(row[0]):
            all_songs[row[0]] = row

    csvfile = open(INPUT2, 'rb')
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        if not all_songs.has_key(row[0]):
            all_songs[row[0]] = row

    csvfile = open(OUTPUT, 'wb')
    writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for song, song_row in all_songs.items():
        writer.writerow(song_row)
