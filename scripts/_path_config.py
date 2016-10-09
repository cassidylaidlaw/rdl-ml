"""Configure the python path to provide access to python packages."""
import sys
from os.path import dirname, realpath, sep, pardir
    
sys.path.append(sep.join([dirname(realpath(__file__)), pardir, 'src-python']))
