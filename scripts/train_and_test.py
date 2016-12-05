import _path_config

import csv
import itertools
import sys

from gensim.models.word2vec import Word2Vec
from rdlml.features import ReturnFeatureExtractor
from rdlml.ml import read_csv_file
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

_, datafname, word2vecfname, testdatafname, resultsfname = sys.argv
X_train, y_train = read_csv_file(datafname)
X_test, y_test = read_csv_file(testdatafname)
word2vec_model = Word2Vec.load(word2vecfname)

feature_names = ["use_word2vec", "use_class", "use_params", "use_method_length"]
feature_sets = [dict(zip(feature_names, use_features)) for use_features in
                itertools.product(*([(False, True)] * len(feature_names)))]

with open(resultsfname, 'w') as resultsfile:
    resultswriter = csv.writer(resultsfile)
    resultswriter.writerow(["word2vec", "class", "params", "method_length", "score"])

    for feature_set in feature_sets:
        feature_extractor = ReturnFeatureExtractor(word2vec_model, **feature_set)
        row = [feature_set[feature] for feature in feature_names]
        model = LogisticRegression()
        pipeline = make_pipeline(feature_extractor, model)
        pipeline.fit(X_train, y_train)
        score = pipeline.score(X_test, y_test)
        row.append(score)
        resultswriter.writerow(row)
