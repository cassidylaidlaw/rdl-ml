import _path_config

import sys
import csv
import os
import subprocess

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 download_github_repos.py repos.csv column outdir')
        print('Downloads all github repositories found in the specified column (0-indexed)')
        print('of repos.csv as URLs and places them in outdir.')
    else:
        _, repos_csv_fname, column_num, outdir = sys.argv
        column_num = int(column_num)
        
        with open(repos_csv_fname, 'r') as repos_csv_file:
            repos_csv = csv.reader(repos_csv_file)
            next(repos_csv) # Skip header row
        
            # Change directories to output directory
            old_cwd = os.getcwd()
            os.chdir(outdir)
        
            for row in repos_csv:
                repo_url = row[column_num]
                subprocess.call(['git', 'clone', '--depth=1', repo_url])
                
            # Change back
            os.chdir(old_cwd)
