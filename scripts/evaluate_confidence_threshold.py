import _path_config

import sys
import pickle
import csv
import os
import numpy as np

from sklearn.pipeline import make_pipeline
from sklearn.ensemble import ExtraTreesClassifier

from rdlml.ml import read_csv_file
from rdlml.features import ReturnFeatureExtractor, ParameterFeatureExtractor

if __name__ == '__main__':
    if len(sys.argv) < 6:
        print('Usage: python3 evaluate_confidence_threshold.py word2vec.pickle (return|params) train.csv test1.csv test2.csv ... out.csv')
        print('Trains a model on train.csv and then evaluates accuracy at various confidence')
        print('levels on the test files.')
    else:
        word2vec_fname, data_type, train_fname = sys.argv[1:4]
        test_fnames = sys.argv[4:-1]
        out_fname = sys.argv[-1]
        
        with open(word2vec_fname, 'rb') as word2vec_file:
            word2vec = pickle.load(word2vec_file)
            
        if data_type == 'return':
            feature_extractor = ReturnFeatureExtractor(word2vec, use_word2vec=False)
        else:
            feature_extractor = ParameterFeatureExtractor(word2vec, use_word2vec=True)
        pipeline = make_pipeline(feature_extractor, ExtraTreesClassifier(100))
        
        train_X, train_y = read_csv_file(train_fname)
        pipeline.fit(train_X, train_y)
        
        confidence_levels = np.arange(0,1.01,0.05)
        columns = [confidence_levels]
        column_headers = ['confidence']
        
        for test_fname in test_fnames:
            test_name = os.path.splitext(os.path.basename(test_fname))[0]
            test_X, test_y = read_csv_file(test_fname)
            probas = pipeline.predict_proba(test_X)
            predicted_col = []
            correct_col = []
            for confidence_level in confidence_levels:
                num_predicted = 0
                num_correct = 0
                for row, correct in zip(probas, test_y):
                    if row.max() >= confidence_level:
                        num_predicted += 1
                        if pipeline.classes_[row.argmax()] == correct:
                            num_correct += 1
                predicted_col.append(num_predicted / test_y.shape[0])
                correct_col.append(num_correct / num_predicted if
                                   num_predicted > 0 else 0)
            column_headers.append('predicted_' + test_name)
            columns.append(predicted_col)
            column_headers.append('correct_' + test_name)
            columns.append(correct_col)
            
        with open(out_fname, 'w') as out_file:
            out = csv.writer(out_file)
            out.writerow(column_headers)
            for row in zip(*columns):
                out.writerow(row)
    