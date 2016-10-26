import _path_config

import sys

from gensim.models.word2vec import Word2Vec

from rdlml.nlp import tokenize_rb_identifier

IDENTIFIER_SENTENCE = 0
FILE_SENTENCE = 1
SENTENCE_TYPES = {'identifier': IDENTIFIER_SENTENCE, 'file': FILE_SENTENCE}

if __name__ == '__main__':
    if len(sys.argv) not in range(3, 5):
        print('Usage: python3 train_word2vec.py identifiers.txt model.pickle (sentence_type)')
        print('Trains a word2vec model over the Ruby identifiers given in identifiers.txt.')
        print('Saves model to model.pickle. sentence_type can either be identifier (default)')
        print('or file. identifier indicates that each identifier should be consider a')
        print('sentence by word2vec, whereas file indicates that an entire file should be.')
    else:
        _, identifiers_fname, model_fname = sys.argv[:3]
        sentence_type = IDENTIFIER_SENTENCE
        if len(sys.argv) >= 4:
            sentence_type = SENTENCE_TYPES[sys.argv[3]]
        
        # Create a corpus of "sentences" for Gensim to train word2vec over
        class IdentifiersCorpus():
            def __iter__(self):
                with open(identifiers_fname, 'r') as identifiers_file:
                    for line in identifiers_file:
                        file_tokens = []
                        for identifier in line.strip().split():
                            tokens = tokenize_rb_identifier(identifier)
                            tokens = [token.lower() for token in tokens]
                            file_tokens.extend(tokens)
                            if sentence_type == IDENTIFIER_SENTENCE:
                                yield tokens
                        if sentence_type == FILE_SENTENCE:
                            yield file_tokens
        
        # Use skip-gram because corpus size is smaller
        model = Word2Vec(IdentifiersCorpus(), sg = 1)
        model.save(model_fname)
        