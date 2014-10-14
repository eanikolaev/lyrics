"""
	example script
	shows how to read songs.csv file
"""

import csv

# set input file name here
INPUT = "songs.csv"


if __name__=='__main__':
    csvfile = open(INPUT, 'rb')
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        print ' '.join(row)

