import _path_config
from os import path
import subprocess
import sys
import re
import json
import csv

#too tired to think of a better of getting classes with type sigs in rdl
ruby_classes = ['Array', 'BasicObject', 'BigDecimal', 'Class', 'Bignum', 'Complex',
 'Date', 'Dir', 'Encoding', 'Enumerable', 'Exception', 'Enumerator', 'File',
 'Stat', 'FileUtils', 'CSV', 'Fixnum', 'Float', 'Hash', 'Integer', 'IO',
 'Kernel', 'Marshal', 'MatchData', 'Math', 'Module', 'NilClass', 'Numeric',
  'Object', 'Pathname', 'Proc', 'Process', 'Random', 'Range', 'Rational',
  'Regexp', 'Set', 'String', 'StringScanner', 'Symbol', 'Time', 'URI']


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

    with open(out_fname, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for ruby_class in ruby_classes:
            types = run_rdl_query(ruby_class) #keys are method name, val is return types
            for k,v in types.items():
                writer.writerow((ruby_class,k,v[0]))
                #made ruby return array of possible types but im just gonna ignore
                #that for now since most only have 1 type to return







#
# for k in cType.method_types:
#     print("name:{},type_sig{}".format(k,cType.method_types[k].type_sig))
