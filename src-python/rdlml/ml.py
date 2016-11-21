
import csv
import numpy as np

def read_csv_file(csv_fname, ignore_first_row = True):
    """
    Reads a CSV file into two numpy arrays X and y. X contains everything but
    the last column and y is the last column. This is useful as training/
    testing data for machine learning algorithms. If ignore_first_row is true,
    then skips the first row of the CSV file (if it's a header, for instance).
    """
    
    X, y = [], []
    with open(csv_fname, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        if ignore_first_row:
            next(csv_reader)
        for row in csv_reader:
            X.append(row[:-1])
            y.append(row[-1])
    return np.array(X), np.array(y)
