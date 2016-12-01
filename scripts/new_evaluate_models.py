import _path_config

import csv
import sys

from gensim.models.word2vec import Word2Vec
from rdlml.ml import read_csv_file
from rdlml.features import ReturnFeatureExtractor
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier

# Build a feature extractor on the word2vec model
_, datafname, word2vecfname, resultsfname = sys.argv
X, y = read_csv_file(datafname)
word2vec_model = Word2Vec.load(word2vecfname)
feature_extractor = ReturnFeatureExtractor(word2vec_model, use_word2vec=True, use_class=True, use_params=False)

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
        pipeline = make_pipeline(feature_extractor, model)
        kfold = KFold(n_splits=10, shuffle=True)
        results = cross_val_score(pipeline, X, y, cv=kfold, scoring="accuracy")
        resultswriter.writerow([name, results.mean(), results.std()])
