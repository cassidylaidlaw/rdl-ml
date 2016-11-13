import csv
import sys

if len(sys.argv) != 2:
    print('Usage: python3 type_stats types.csv')
    print('outputs stats for a csv of type signatures')
else:
    _, fname = sys.argv
    reader = csv.reader(open(fname, 'r'))
    d = {}
    counts_dict ={}
    for row in reader:
        c,m, r = row #class,method,return type
        if c in d:
            d[c].append((m,r))
        else:
            d[c] = [(m,r)]

        if r in counts_dict:
            counts_dict[r]+=1
        else:
            counts_dict[r] = 1

    counts = []
    for k,v in counts_dict.items():
        counts.append((k,v))
    counts.sort(key=lambda x: x[1],reverse=True)
    print(str(counts))
