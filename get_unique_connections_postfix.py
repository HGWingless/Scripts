# I pull all of the unique host names that connected out of postfix logs and write them to an output file
# 20220120 - jparmely
# Change your in and out files here, if applicable
open_this = 'mail.log'
output_here = 'out.txt'

matches = []
with open(open_this, 'r') as f:  # Open the log file
    with open(output_here, 'w') as o:  # Open the outfile, as writable (overwrite each time)
        line = f.readline()
        while line:  # Until we run out of lines, look for disconnect
            if 'disconnect' in line:
                split = line.split(':')  # Run a split to get to the host information
                split2 = split[3].split()  # Split last split to keep only the host and IP address
                matches.append(split2[2])  # Put the results in a list
            line = f.readline()
        myset = set(matches)  # Sets are unique - This removes the duplicates for us
        for i in myset:  # Write the contents of the set to the outfile with a newline after each entry
            o.write(i + '\n')