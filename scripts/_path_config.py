"""Configure the python path to provide access to python packages."""
import sys
from os.path import dirname, realpath, sep, pardir
    
sys.path.append(sep.join([dirname(realpath(__file__)), pardir, 'src-python']))

# Get ruby source directory if needed
src_ruby = sep.join([dirname(realpath(__file__)), pardir, 'src-ruby'])

# Configure logging as well while we're at it
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

