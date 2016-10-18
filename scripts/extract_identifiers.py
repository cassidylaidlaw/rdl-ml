import _path_config

import sys
from os import path
import subprocess
import logging
import glob

EXTRACT_IDENTIFIERS_RB = path.sep.join([_path_config.src_ruby,
                                        'extract_identifiers.rb'])

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 extract_identifiers rubydir out.txt')
        print('Extract all identifiers from all ruby files in rubydir and write them to the')
        print('given output file, one identifier per line.')
    else:
        _, ruby_dir, out_fname = sys.argv
        ruby_files = glob.glob(path.sep.join([ruby_dir, '**', '*.rb']),
                               recursive = True)
        with open(out_fname, 'w') as out_file:
            for ruby_file in ruby_files:
                logging.info('extracting identifiers from %s', ruby_file)
                subprocess.run(['ruby', EXTRACT_IDENTIFIERS_RB, ruby_file],
                               stdout = out_file)
