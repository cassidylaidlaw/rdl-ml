import _path_config

import sys

from collections import Counter
from rdlml.ml import read_csv_file

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 type_stats types.csv')
        print('Outputs stats for a CSV of type information')
    else:
        _, csv_fname = sys.argv
        
        X, y = read_csv_file(csv_fname)
        type_counts = Counter(y)
        for type, count in sorted(type_counts.items(), key = lambda i: i[1],
                                  reverse = True):
            print('{}: {} occurences ({:.1f}%)'.format(type, count,
                    count / len(y) * 100))
        print('Total: {} occurences'.format(len(y)))
