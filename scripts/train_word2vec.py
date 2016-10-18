import _path_config

import sys

from gensim.models.word2vec import Word2Vec

from rdlml.nlp import tokenize_rb_identifier

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 train_word2vec.py identifiers.txt model.pickle')
        print('Trains a word2vec model over the Ruby identifiers given in identifiers.txt.')
        print('Saves model to model.pickle.')
    else:
        _, identifiers_fname, model_fname = sys.argv
        
        # Create a corpus of "sentences" for Gensim to train word2vec over
        class IdentifiersCorpus():
            def __iter__(self):
                with open(identifiers_fname, 'r') as identifiers_file:
                    for line in identifiers_file:
                        tokens = tokenize_rb_identifier(line.strip())
                        tokens = [token.lower() for token in tokens]
                        yield tokens
        
        model = Word2Vec(IdentifiersCorpus())
        model.save(model_fname)
        