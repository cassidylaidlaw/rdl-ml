import subprocess
import _path_config
from _parse_type_sigs import parse_sigs
import os
import sys
import json
import csv
import re
GUESS_TYPES_RB = os.path.sep.join([_path_config.src_ruby,'guess_types.rb'])
MERGE_JSON = os.path.sep.join([_path_config.src_ruby,'merge_json.rb'])

if len(sys.argv) != 3:
    print('Usage: python3 guess_ruby_types.py ruby_folder out_folder')
    exit()

_, ruby_folder, out_folder_name = sys.argv
out_fname = "{}/guess.json".format(out_folder_name)
with open(out_fname, 'w') as out_file:
    out_file.write("{}")


def run_ruby(ruby_fname):
#   out_fname = "{}/{}.json".format(out_folder_name,ruby_fname)
    ruby_file_path = "{}/{}".format(ruby_folder,ruby_fname)
    print("running {}, to {}".format(ruby_file_path,out_fname))
    output = subprocess.run(['ruby', GUESS_TYPES_RB, ruby_file_path,out_fname],
                stdout = subprocess.PIPE).stdout.decode("utf-8")
    #print(output)

for file in os.listdir(ruby_folder):
    if file.endswith(".rb"):
        run_ruby(file)
#merge json
output = subprocess.run(['ruby', MERGE_JSON, out_fname,out_fname],
            stdout = subprocess.PIPE).stdout.decode("utf-8")
