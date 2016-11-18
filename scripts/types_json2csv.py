import _path_config

import sys
import json
import csv
from rdlml.ruby import generalize_type

if __name__ == '__main__':
    if len(sys.argv) != 4 or sys.argv[3] not in ['return', 'params']:
        print('Usage: python3 types_json2csv.py types.json types.csv (return|params)')
        print('Given a JSON file of observed types from running a test suite, outputs a CSV')
        print('file that can be used as training/testing data for a ML algorithm. Either')
        print('outputs a CSV file with data on the return types or parameter types depending')
        print('on the third command-line argument.')
    else:
        _, json_fname, csv_fname, data_type = sys.argv
        
        with open(json_fname, 'r') as json_file:
            json_data = json.load(json_file)
        
        with open(csv_fname, 'w') as csv_file:
            csv_out = csv.writer(csv_file)
            
            # Write header row
            if data_type == 'return':
                csv_out.writerow(['Method name', 'Class name',
                                  'Parameter names', 'Return type'])
            else:
                csv_out.writerow(['Parameter name', 'Method name',
                                  'Class name', 'Parameter type'])
            
            for class_name, methods in json_data.items():
                for method_name, method_data in methods.items():
                    # Get return type information
                    if 'ret_types' in method_data:
                        return_type = method_data['ret_types'][0]
                        return_type = generalize_type(return_type)
                    else:
                        return_type = None
                        
                    # Get parameter name/return type information
                    if 'parameter_names' in method_data:
                        parameter_names = [param for param in
                                method_data['parameter_names'] if param != '']
                    else:
                        parameter_names = []
                    if 'parameter_types' in method_data:
                        parameter_types = [types[0] for types in
                                           method_data['parameter_types']]
                        parameter_types = list(map(generalize_type,
                                                   parameter_types))
                    else:
                        parameter_types = []
                    
                    # Write rows to CSV
                    if data_type == 'return':
                        if return_type is not None:
                            csv_out.writerow([method_name, class_name,
                                              ','.join(parameter_names),
                                              return_type])
                    else:
                        for parameter_name, parameter_type in \
                                zip(parameter_names, parameter_types):
                            csv_out.writerow([parameter_name, method_name,
                                              class_name, parameter_type])
