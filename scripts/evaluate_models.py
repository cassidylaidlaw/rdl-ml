import _path_config

import csv
import numpy as np
import random
import sys

from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python naive_bayes.py <dataset>")
        sys.exit()

    # Load data from csv file into lists
    _, input_csv = sys.argv
    vectors = list()
    return_types = list()
    with open(input_csv, 'r') as data_file:
        data_reader = csv.reader(data_file)
        for row in data_reader:
            vectors.append(row[0:100])
            return_types.append(row[100])

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

    # Let's run our models!
    for name, model in models:
        kfold = cross_validation.KFold(n=len(vectors), n_folds=10, random_state=11)
        results = cross_validation.cross_val_score(model, vectors, return_types, cv=kfold, scoring="accuracy")
        print("%s: mean %f stdev %f" % (name, results.mean(), results.std()))

