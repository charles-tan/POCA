import csv
import json
import sys

csvfile = open(sys.argv[1], 'r')
jsonfile = open(sys.argv[2], 'w')
csv_headings = next(csvfile)

fieldnames = csv_headings.split(',')

reader = csv.DictReader( csvfile, fieldnames)
out = json.dumps([row for row in reader], indent=4)
jsonfile.write(out)

