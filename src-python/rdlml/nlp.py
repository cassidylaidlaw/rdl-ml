
import string

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
