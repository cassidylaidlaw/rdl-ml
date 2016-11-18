"""
Convenience methods for working with ruby types
"""

BASIC_RUBY_TYPES = ['Integer', 'Numeric', 'Bool', 'Array', 'String',
                    'self', 'Enumerator', 'nil',
                    '%any', 'Hash', 'Time', 'Set', 'Symbol']

def generalize_type(t):
    """
    Given a type t, generalize it to a number of basic Ruby types in order to
    make fewer classes for the machine learning algorithms to work over.
    """
    
    # Generalize subclasses of Integer to Integer
    if t in ['Bignum', 'Fixnum']:
        return 'Integer'
    # Generalize other Numeric types to Numeric
    if t in ['Complex', 'Rational', 'Float']:
        return 'Numeric'
    
    # Convert NilClass -> nil
    if t == 'NilClass':
        return 'nil'
    
    # Otherwise, if t is not a basic Ruby type then return 'Object'
    if t in BASIC_RUBY_TYPES:
        return t
    else:
        return 'Object'
