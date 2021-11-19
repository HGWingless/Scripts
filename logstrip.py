# This script takes a file (designed to be a proxy log CSV from Synology) and creates a new file, minus the lines
# containing text you put in the list (like 403 errors). This was built because pihole causes a ton
# of log flood when telemetry fails to connect to its remote end.
import argparse
from pathlib import Path

# Build a parser (Require infile, accept outfile, with a default)
parser = argparse.ArgumentParser(
    prog='logstrip', description='Strip 403 error lines out of proxy log CSVs from Synology so you can actually read '
                                 'them.')
parser.add_argument("Path", type=Path, help="Path to in file")
parser.add_argument("-o", '--outfile', type=Path, help="Path to output file", default='./cleaned.csv')
p = parser.parse_args()

# Change this list to change how we remove lines. Remember, we match based on ANY
remove_this = ['403']

# Open infile, open outfile (writable). If we don't get hits from our removal list, write to the outfile
with open(p.Path) as f, open(p.outfile, 'w') as c:
    for line in f:
        if not any(bad_word in line for bad_word in remove_this):
            c.write(line)

print('Output file successfully created at: ' + str(p.outfile))
