import subprocess
import _path_config
from _parse_type_sigs import parse_sigs
from os import path
import sys
import json
import csv
GUESS_TYPES_RB = path.sep.join([_path_config.src_ruby,'guess_types.rb'])


if len(sys.argv) != 3:
    print('Usage: python3 guess_ruby_types.py ruby_file.rb out.csv')
    #TODO: runs tests in other specifed ruby file to get types at runtime for those classes'
    print('Uses rdl_guesstypes on the classes define in ruby_file.rb')
    print('outputs as csv to specifed output file')
    exit()

_, ruby_fname, out_fname = sys.argv

output = subprocess.run(['ruby', GUESS_TYPES_RB, ruby_fname],
            stdout = subprocess.PIPE).stdout.decode("utf-8")



output = json.loads(output)
with open(out_fname, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for klass,types in output.items():
        sigs = parse_sigs(types)
        for sig in sigs:
            writer.writerow([klass]+sig)
    #sigs = parse_sigs(types)
