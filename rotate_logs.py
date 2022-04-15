# This script rotates the awstats log file in hmail when run. Its intent is to be run as a scheduled task once a week to
# coincide with when error reporting is run, otherwise, we will end up reporting on the same data set repeatedly.
# hmailserver_awstats.log will end up being hmailserver_awstats.log.1, 1 will be 2, and so on. .5 is intended to be
# deleted by the purge script when it runs.
# v1.0 20220208

# IF YOU WANT MAIL TO WORK, UNCOMMENT THE FUNCTION CALL AT THE BOTTOM AND UPDATE THE TO/FROM VARIABLES BELOW.

import os
from os.path import exists as file_exists
from pathlib import Path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Fill in here to have a sender/recipient for the results email an a subject
MAIL_TO = ''
MAIL_FROM = ''
email_subject = ''  # Technically optional, but...
#######################
BASE_PATH = 'C:\Program Files (x86)\hMailServer\Logs'  # These are default for hmail w/ awstats enabled 
LOG_FILE = '\hmailserver_awstats.log'
log = []
counter = 4
# Rotate hmailserver_awstats.log.# one number forward and log the results. Keeps 1 month of historical,
# the active log, and a .5 log, which will get purged on schedule by other scripts if present.
for i in range(4):
    # If this file exists, rename it one number higher and log
    if file_exists(BASE_PATH + LOG_FILE + '.' + str(counter)):
        os.rename(BASE_PATH + LOG_FILE + '.' + str(counter), BASE_PATH + LOG_FILE + '.' + str(counter + 1))
        log.append("Renamed " + BASE_PATH + LOG_FILE + '.' + str(counter) + ' to ' + BASE_PATH + LOG_FILE + '.' + str(counter + 1))
    else:
        # Else, log that we skipped it
        log.append(BASE_PATH + LOG_FILE + '.' + str(counter) + ' - File NOT Found')
    counter = counter - 1  # Increment counter
# Finally, move the main log to .1 and log. Post exception if this fails for some reason
if file_exists(BASE_PATH + LOG_FILE):
    os.rename(BASE_PATH + LOG_FILE, BASE_PATH + LOG_FILE + '.' + str('1'))
    log.append(
        "Renamed " + BASE_PATH + LOG_FILE + ' to ' + BASE_PATH + LOG_FILE + '.' + str('1'))
else:
    log.append(BASE_PATH + LOG_FILE + ' - File NOT Found')
# The working file probably gets recreated on its own, but just in case...
if file_exists(BASE_PATH + LOG_FILE):
    log.append('Working file already exists. Touch not being run.')
else:
    Path(BASE_PATH + LOG_FILE).touch()
    log.append('Running touch on working file.')
# Send out script results so I know if everything is working
def send_error_mail():
    body_string = ''
    for i in log:
        body_string = body_string + i + '\n'
    message_body = body_string
    msg = MIMEMultipart()
    body_part = MIMEText(message_body, 'plain')
    msg['Subject'] = email_subject
    msg['From'] = MAIL_FROM
    msg['To'] = MAIL_TO  # Whomever maintains this long-term
    # Add body to email
    msg.attach(body_part)
    # Since this runs on the local mail server, we should be able to send this as SMTP locally. Change if not accurate.
    sent = smtplib.SMTP('localhost', 25)
    sent.sendmail(msg['From'], msg['To'], msg.as_string())
    sent.quit()

#send_error_mail() # UNCOMMENT ME TO SEND MAIL