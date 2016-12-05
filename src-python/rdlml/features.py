
from collections import Counter

from sklearn.base import BaseEstimator, TransformerMixin
from scipy.sparse import csr_matrix
import scipy.sparse
import numpy as np

from .nlp import tokenize_rb_identifier, identifier2vec

class FeatureExtractor(BaseEstimator, TransformerMixin):
    """
    A scikit-learn transformer that allows for a number of ways to extract
    features from data on either return types or parameter types. This is an
    abstract class so instantiate one of it's subclasses.
    """
    
    def __init__(self, word2vec, use_word2vec=True):
        """
        Initialize with a word2vec model and whether to use a word2vec
        representation of words or just a sparse vector representation.
        """
        
        self.word2vec = word2vec
        self.use_word2vec = use_word2vec
        
        self.max_word_index = max(vocab.index for vocab in
                                  self.word2vec.vocab.values())
        
    def _get_features(self, row):
        """
        Subclasses override this to provide a list of either numerical or
        textual features. If a feature is textual, it is further transformed
        by the transform method to turn it into a word2vec or word count
        vector.
        """
        
        raise NotImplementedError()
    
    def _count_vectorize(self, s):
        """
        Given a string s, tokenize it, count the tokens, and return a sparse
        count vector representation.
        """
        
        indptr = [0]
        indices = []
        data = []
        
        counts = Counter(tokenize_rb_identifier(s))
        for word, count in counts.items():
            if word in self.word2vec.vocab:
                indices.append(self.word2vec.vocab[word].index)
                data.append(count)
        indptr.append(len(indices))
            
        return csr_matrix((data, indices, indptr),
                          shape=(1, self.max_word_index + 1), dtype=float)
        
    def fit(self, X, y = None):
        return self
    
    def transform(self, X):
        Xt = []
        # Use numpy if we're using dense matrices, else use scipy.sparse
        fn = np if self.use_word2vec else scipy.sparse
        array = np.array if self.use_word2vec else csr_matrix
        for row in X:
            features = self._get_features(row)
            feature_vectors = []
            for feature in features:
                if isinstance(feature, str):
                    if self.use_word2vec:
                        feature_vectors.append(identifier2vec(feature,
                                                              self.word2vec))
                    else:
                        feature_vectors.append(self._count_vectorize(feature))
                else:
                    feature_vectors.append(array([float(feature)] *
                            self.word2vec.vector_size))
            feature_vector = fn.hstack(feature_vectors)
            Xt.append(feature_vector)
        return fn.vstack(Xt)

class ReturnFeatureExtractor(FeatureExtractor):
    
    def __init__(self, word2vec, use_word2vec=True, use_class=False,
                 use_params=False, use_method_length=False):
        super().__init__(word2vec, use_word2vec)
        self.use_class = use_class
        self.use_params = use_params
        self.use_method_length = use_method_length
        
    def _get_features(self, row):
        method_name, class_name, params, method_length = row
        features = [method_name]
        if self.use_class:
            features.append(class_name)
        if self.use_params:
            params = params.split(',')
            features.append(len(params))
            features.append('_'.join(params))
        if self.use_method_length:
            features.append(method_length)
        return features
    
class ParameterFeatureExtractor(FeatureExtractor):
    
    def __init__(self, word2vec, use_word2vec=True, use_method=False,
                 use_class=False, use_method_length=False):
        super().__init__(word2vec, use_word2vec)
        self.use_method = use_method
        self.use_class = use_class
        self.use_method_length = use_method_length
        
    def _get_features(self, row):
        parameter_name, method_name, class_name, method_length = row
        features = [parameter_name]
        if self.use_method:
            features.append(method_name)
        if self.use_class:
            features.append(class_name)
        if self.use_method_length:
            features.append(method_length)
        return features
        