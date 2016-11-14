import _path_config

import csv
import logging
import os
import sys

from gensim.models.word2vec import LineSentence
from gensim.models.word2vec import Word2Vec

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))

model = Word2Vec(LineSentence("identifiers.txt"), size=400, window=5, min_count=1)
model.init_sims(replace=True)

with open("../datasets/class-mname-rettype.csv", 'r') as infile:
    with open("../datasets/vectors_returntypes.csv", 'w', newline='') as outfile:
        inreader = csv.reader(infile)
        outwriter = csv.writer(outfile)
        for line in inreader:
            v = model[line[1].strip()].tolist()
            v.append(line[2].strip())
            outwriter.writerow(v)
