#pip install naked (0.1.31) and make sure rdl gem is installed

import sys
from Naked.toolshed.shell import muterun_rb

if len(sys.argv)<2:
    print("Specify ruby file to run")
    exit()

response = muterun_rb(sys.argv[1])
if response.exitcode == 0:
  print(response.stdout.decode("utf-8"))
else:
  sys.stderr.write(response.stderr)
