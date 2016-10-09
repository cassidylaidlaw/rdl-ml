import _path_config

import sys
import re
import requests
import csv

README_URL = 'https://raw.githubusercontent.com/ekremkaraca/awesome-rails/master/README.md'
MARKDOWN_TABLE_RE = re.compile(r'\|(.*)\|(.*)\|(.*)\|')
MARKDOWN_LINK_RE = re.compile(r'\[(\w*)\]\(([^\)]*)\)')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 scrape_awesome_rails.py out.csv')
        print('Scrape the awesome-rails GitHub repository and output information about the')
        print('Rails applications mentioned to the given CSV file.')
    else:
        _, out_fname = sys.argv
        
        with open(out_fname, 'w') as out_file:
            csv_out = csv.writer(out_file)
            csv_out.writerow(['Name', 'Description', 'GitHub URL', 'Live URL'])
            readme_text = requests.get(README_URL).text
            for table_match in MARKDOWN_TABLE_RE.finditer(readme_text):
                cols = tuple(c.strip() for c in table_match.groups())
                if cols == ('Name', 'Description', 'Link'):
                    pass
                # If only character is '-', ignore
                elif ''.join(set(''.join(cols))) == '-':
                    pass
                else:
                    name_col, description, link_col = cols
                    name_match = MARKDOWN_LINK_RE.match(name_col)
                    link_match = MARKDOWN_LINK_RE.match(link_col)
                    if name_match and link_match:
                        name = name_match.group(1)
                        github_url = name_match.group(2)
                        live_url = link_match.group(2)
                        csv_out.writerow([name, description, github_url,
                                          live_url])
