import datetime
import os
import json
import csv

with open("a.csv","r") as csvfile:
    with open("a.log", "w") as ostream:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            ostream.write('#'.join(row) + '\n')
    ostream.close()
csvfile.close()