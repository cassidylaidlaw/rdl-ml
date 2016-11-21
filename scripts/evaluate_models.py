import _path_config

import csv
import logging
import numpy as np
import os
import random
import sys

from gensim.models.word2vec import Word2Vec
from rdlml.nlp import tokenize_rb_identifier
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier

if len(sys.argv) != 4:
    print("Usage: python3 evaluate_models.py <model.pickle> <dataset.csv> <results.csv>")
    sys.exit()

# Load the pretrained Word2vec model
_, modelfname, datasetfname, resultsfname = sys.argv
word2vec_model = Word2Vec.load(modelfname)

# Load method names and return types into two lists
method_names = list()
return_types = list()
with open(datasetfname, 'r') as datafile:
    # datareader = csv.DictReader(datafile)
    datareader = csv.reader(datafile)
    for row in datareader:
        # method_names.append(row["Method name"])
        method_names.append(row[1])
        # return_types.append(row["Return type"])
        return_types.append(row[2])

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

# Run the models using cross validation and write results to file
with open(resultsfname, 'w') as resultsfile:
    resultswriter = csv.writer(resultsfile)
    resultswriter.writerow(["model", "mean", "stdev"])
    for name, model in models:
        kfold = KFold(n_splits=2, shuffle=True)
        results = cross_val_score(model, vectors, return_types, cv=kfold, scoring="accuracy")
        resultswriter.writerow([name, results.mean(), results.std()])
