import csv
import numpy as np
import sys

from sklearn import cross_validation
from sklearn.naive_bayes import GaussianNB

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python naive_bayes.py <dataset>")
        sys.exit()

    _, input_csv = sys.argv
    vectors = list()
    return_types = list()
    with open(input_csv, 'r') as data_file:
        data_reader = csv.reader(data_file)
        for row in data_reader:
            vectors.append(row[0:100])
            return_types.append(row[100])

    vectors = np.array(vectors).astype(np.float)
    return_types = np.array(return_types)

    classifier = GaussianNB()
    kfold = cross_validation.KFold(n=len(vectors), n_folds=10)
    cv_results = cross_validation.cross_val_score(classifier, vectors, return_types, cv=kfold, scoring="accuracy")

    print(cv_results.mean())
    print(cv_results.std())
