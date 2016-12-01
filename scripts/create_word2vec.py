import _path_config

import csv
import logging
import os
import sys

from gensim.models.word2vec import Word2Vec
from rdlml.nlp import tokenize_rb_identifier

if len(sys.argv) != 3:
    print("Usage: python3 create_word2vec.py <dataset.csv> <model.pickle>")
    sys.exit()

# Store method names and return types in two lists
_, datafname, modelfname = sys.argv
method_names = list()
class_names = list()
#parameter_names = list()
return_types = list()
with open(datafname, 'r') as data_file:
    data_reader = csv.DictReader(data_file)
    for row in data_reader:
        method_names.append(row["Method name"])
        class_names.append(row["Class name"])
        #parameter_names.append(row["Parameter names"].split(','))
        return_types.append(row["Return type"])

# Put all method names together with tokens in a list
tokenized_method_names = list()
for method_name, class_name in zip(method_names, class_names):
    tokens = tokenize_rb_identifier(method_name)
    tokens.append(class_name)
    tokens += tokenize_rb_identifier(class_name)
    #for name in parameter_name:
    #   if name != '':
    #       tokens += tokenize_rb_identifier(name)
    if method_name not in tokens:
        tokens = [method_name] + tokens

    tokenized_method_names.append(tokens)

# Train a Word2vec model on tokenized_method_names and save it
program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
word2vec_model = Word2Vec(tokenized_method_names, size=200, min_count=1, sg=1, hs=1)
word2vec_model.save(modelfname)
