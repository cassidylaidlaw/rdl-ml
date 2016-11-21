import _path_config

import csv
import logging
import numpy as np
import os
import random
import sys

from gensim.models.word2vec import Word2Vec
from rdlml.nlp import tokenize_rb_identifier
from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier

if len(sys.argv) != 2:
    print("Usage: python evaluate_models.py <dataset.csv>")
    sys.exit()

# Store method names and return types in two lists
_, datafname = sys.argv
method_names = list()
return_types = list()
with open(datafname, 'r') as data_file:
    data_reader = csv.reader(data_file)
    for row in data_reader:
        method_names.append(row[1])
        return_types.append(row[2])

# Put all method names together with tokens in a list
tokenized_method_names = list()
for method_name in method_names:
    tokens = tokenize_rb_identifier(method_name)
    if method_name not in tokens:
        tokens = [method_name] + tokens
    tokenized_method_names.append(tokens)

# Train a Word2vec model on tokenized_method_names
program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
word2vec_model = Word2Vec(tokenized_method_names, size=50, min_count=1, sg=1, hs=1)

# Create list of vectors using Word2vec model
vectors = list()
for method_name in method_names:
    vectors.append(word2vec_model[method_name])

# Convert lists to numpy arrays
vectors = np.array(vectors).astype(np.float)
return_types = np.array(return_types)

# Create a bunch of models that we're going to evaluate
models = list()
models.append(("Logistic Regression", LogisticRegression()))
models.append(("K Nearest Neighbors", KNeighborsClassifier()))
models.append(("Decision Tree Classifier", DecisionTreeClassifier()))
models.append(("Naive Bayes", GaussianNB()))
models.append(("Support Vector Machine", SVC()))
models.append(("Random Forest Classifier", RandomForestClassifier()))
models.append(("Extra Trees Classifier", ExtraTreesClassifier()))

# Let's run our models!
for name, model in models:
    kfold = cross_validation.KFold(n=len(vectors), n_folds=10, shuffle=True)
    results = cross_validation.cross_val_score(model, vectors, return_types, cv=kfold, scoring="accuracy")
    print("%s: mean %f stdev %f" % (name, results.mean(), results.std()))
