# This script should run daily to help us keep about a month worth of hmail logs. Hmail only rotates with out pruning,
# so we have to do it on our own.
# Hmail keeps a daily, full log by default, and we are splitting our awstats log into weekly chunks already for
# Similified reporting. Modify to fit your retention requirements
# v1.0 20220201
# Update 20220208 - Added functionality to purge the oldest awstats log
from datetime import datetime, timedelta
import os
date_range = []
today = datetime.now()
datestr = today.strftime("%Y-%m-%d")
file_name = ''
# Get the dates for the last month in yyyymmdd format.
for x in range(30):
    # first time x = 1, if today's date is Feb 18, then it's Feb 17
    within_week = today - timedelta(days=x+2)  # x+2 makes sure we keep it at about 30 days
    # Take this information and put it in the format that hmail logs are created
    within_week = within_week.strftime("%Y-%m-%d")
    date_range.append(within_week)
# Generate what the file name is going to be for a given date (a month ago)
file_name = 'C:\Program Files (x86)\hMailServer\Logs\hmailserver_' + date_range[29] + '.log'
# Try to delete the log file from a month ago, and broadly catch the error if we can't
try:
    os.remove(file_name)
    print(file_name + " was deleted.")
except:
    print("Couldn't delete " + file_name + ". This probably means it doesn't exist anyway.")
try:
    # If over a month of historical awstats logs exist, purge the .5. This should only happen weekly
    os.remove('C:\Program Files (x86)\hMailServer\Logs\hmailserver_awstats.log.5')
except:
    print("Couldn't delete C:\Program Files (x86)\hMailServer\Logs\hmailserver_awstats.log.5"
          " This probably means it doesn't exist anyway.")