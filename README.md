# Scripts
Misc. scripts and code projects go here.
------------------

check_mullvad - See if your Mullvad vpn is still running, and try to restart it if not. If that fails, shut down a list of services

check_omocat - This was half a joke script, but it can be repurposed to see when a website is still in maint. mode (redirects you somewhere)

get_unique_connections_postfix - Scrub through a postfix mail log and get a unique list of all clients that connected to it

logstrip - Parse a Synology proxy log and remove lines based on criteria that you set. Useful if you get a ton of errors due to DNS filtering

purge_logs - Prunes logs to (default) 30 days or so. Designed for use in hmail, which includes dates in their file names but can probably be tweaked for any system.

rotate_logs - Sister to purge_logs. Splits the awstats logs into week-long chunks.
