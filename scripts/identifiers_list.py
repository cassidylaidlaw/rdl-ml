import _path_config

import csv
import sys

from rdlml.nlp import tokenize_rb_identifier

with open("identifiers.txt", 'w') as outfile:
    with open(sys.argv[1], 'r') as inputcsv:
        data_reader = csv.reader(inputcsv)
        for row in data_reader:
            tokens = [row[1]] + tokenize_rb_identifier(row[1])
            outfile.write(" ".join(tokens))
            outfile.write("\r\n")

