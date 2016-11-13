import _path_config
from _parse_type_sigs import parse_sigs
from os import path
import subprocess
import sys
import re
import json
import csv

#too tired to think of a better of getting classes with type sigs in rdl
ruby_classes = ['Array', 'BasicObject', 'BigDecimal', 'Class', 'Bignum', 'Complex',
 'Date', 'Encoding', 'Enumerable', 'Exception', 'Enumerator',
 'Stat', 'FileUtils', 'CSV', 'Fixnum', 'Float', 'Hash', 'Integer',
 'Marshal', 'MatchData', 'Math', 'Module', 'NilClass', 'Numeric',
  'Object',  'Proc', 'Process', 'Random', 'Range', 'Rational',
  'Regexp', 'Set', 'String', 'StringScanner', 'Symbol', 'Time']

#these classes have a good amount of none standard return values so ill
#deal with these later
# 'Kernel',  'File',  'Dir', 'URI', 'IO', 'Pathname',

GET_TYPES_RB = path.sep.join([_path_config.src_ruby,'get_types.rb'])


def run_rdl_query(ruby_class_name):
    print("running: " + ruby_class_name)
    output = subprocess.run(['ruby', GET_TYPES_RB, ruby_class_name],
                stdout = subprocess.PIPE).stdout.decode("utf-8")
    return json.loads(output)


if len(sys.argv) != 2:
    print('Usage: python3 scrape_ruby_types out.csv')
    print('Uses rdl_query to get type info for all core types with type signatures')
    print('outputs as csv to specifed output file')
else:
    _, out_fname = sys.argv
    polymorphic = re.compile("[tuvk]$")
    otherInfo = re.compile("^(.+) (.+)")
    #some types returned are in format '<type> <info about type> so this will remove the info'
    with open(out_fname, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for ruby_class in ruby_classes:
            types = run_rdl_query(ruby_class) #keys are method name, val is return types
            sigs = parse_sigs(types)
            for sig in sigs:
                writer.writerow([ruby_class]+sig)
