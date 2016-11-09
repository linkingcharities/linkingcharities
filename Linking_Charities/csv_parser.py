import csv
import sys

from charity.models import *

file = sys.argv[0]

with open(file, 'rt') as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
        for field in row:
            if field = 
