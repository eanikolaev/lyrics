"""
    example script
    shows how to read songs.csv file
"""

import csv

# set input and output file names here
INPUT  = "songs.csv"
OUTPUT = "test_texts_of_songs.csv"


if __name__=='__main__':
    in_csvfile = open(INPUT, 'rb')
    reader = csv.reader(in_csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    out_csvfile = open(OUTPUT, 'wb')
    writer = csv.writer(out_csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for row in reader:
        writer.writerow(row[-2:-1])

