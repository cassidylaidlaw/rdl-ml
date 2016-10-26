
import string

import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin

def tokenize_rb_identifier(identifier):
    """
    Given a Ruby identifier, tokenizes it and returns a resulting list of
    strings.
    """
    
    underscore_tokens = identifier.split('_')
    tokens = []
    for token in underscore_tokens:
        token_start = 0
        for index, char in enumerate(token):
            if char in string.ascii_uppercase:
                token_starts_here = True
            elif char in string.ascii_lowercase or char in '0123456789':
                token_starts_here = False
            else:
                token_starts_here = True
                
            if token_starts_here:
                new_token = token[token_start:index]
                if new_token != '':
                    tokens.append(new_token)
                token_start = index
        tokens.append(token[token_start:])
                
    return tokens

def identifier2vec(identifier, word2vec):
    """
    Given an identifier and a gensim word2vec mode, returns a vector that
    represents the identifier. Works by taking an average of the vectors for
    the individual tokens in the identifier.
    """
    
    # Start with the zero vector
    vector = np.zeros(word2vec.syn0.shape[1])
    token_count = 0
    
    for token in tokenize_rb_identifier(identifier):
        try:
            vector += word2vec[token]
            token_count += 1
        except KeyError:
            pass
    
    if token_count > 0:
        vector /= token_count
    
    return vector

class Word2VecTransformer(BaseEstimator, TransformerMixin):
    """
    Transforms ruby identifiers (strings) to vectors using word2vec and the
    identifier2vec method described above.
    """
    
    def __init__(self, word2vec):
        """
        Initialize with the given Gensim word2vec model.
        """
        
        super().__init__()
        self.word2vec = word2vec
    
    def fit(self, X, y = None):
        return self
        
    def transform(self, X, y = None):
        return np.vstack([identifier2vec(identifier, self.word2vec)
                          for identifier in X])

