import _path_config

import csv
import sys
import itertools
import logging

from gensim.models.word2vec import Word2Vec
from rdlml.ml import read_csv_file
from rdlml.features import ReturnFeatureExtractor
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
import numpy as np

# Build a feature extractor on the word2vec model
_, datafname, word2vecfname, resultsfname = sys.argv
X, y = read_csv_file(datafname)
word2vec_model = Word2Vec.load(word2vecfname)

# Create a bunch of models that we're going to evaluate
models = list()
models.append(("Logistic Regression", LogisticRegression()))
models.append(("K Nearest Neighbors", KNeighborsClassifier()))
models.append(("Decision Tree Classifier", DecisionTreeClassifier()))
models.append(("Naive Bayes", MultinomialNB()))
models.append(("Support Vector Machine", SVC()))
models.append(("Random Forest Classifier", RandomForestClassifier()))
models.append(("Extra Trees Classifier", ExtraTreesClassifier()))

# Create feature sets to evaluate
feature_names = ['use_word2vec', 'use_class', 'use_params']
feature_sets = [dict(zip(feature_names, use_features)) for use_features in
                itertools.product(*([(False, True)] * len(feature_names)))]
feature_sets = feature_sets[-1:]

# Run the models using cross validation and write results to file
with open(resultsfname, 'w') as resultsfile:
    resultswriter = csv.writer(resultsfile)
    
    # Write headers
    resultswriter.writerow(feature_names + list(itertools.chain(
            *[[model_name, ""] for model_name, _ in models])))
    resultswriter.writerow([""] * len(feature_names) +
                           ["mean", "stdev"] * len(models))
    for feature_set in feature_sets:
        feature_extractor = ReturnFeatureExtractor(word2vec_model,
                                                   **feature_set)
        feature_set_str = ', '.join('{}={}'
                .format(feature, use) for feature, use in
                feature_set.items())
        row = [feature_set[feature] for feature in feature_names]
        for name, model in models:
            logging.info("testing {} with {}".format(feature_set_str, name))
            # Switch to Guassian NB for word2vec data
            if name == 'Naive Bayes' and feature_set['use_word2vec']:
                model = GaussianNB()
            
            pipeline = make_pipeline(feature_extractor, model)
            kfold = KFold(n_splits=10, shuffle=True)
            results = cross_val_score(pipeline, X, y, cv=kfold, scoring="accuracy")
            row.extend([results.mean(), results.std(ddof=1)])
            logging.info("mean accuracy={:.3f} stdev={:.3f}".format(results.mean(),
                    results.std(ddof=1)))
        resultswriter.writerow(row)
