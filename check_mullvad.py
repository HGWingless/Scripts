# I am script to see if we are still connected to our VPN. If we're not, we try to restart the ovpn service
# associated with it. If not, we stop dependent services and wait for manual intervention
# Critical log entries are caught by my syslog server, so notifications are made
# v1.0 - 20220318
import os
import subprocess
import time

# FILL THESE IN FOR SERVICES TO STOP IF SERVICES CAN'T BE RECOVERED
restart_me = ''
###################################
def check_mullvad():
	# This hits the site used to check for connection to Mullvad's back end and parses a good condition
    proxycheck = subprocess.Popen("curl https://am.i.mullvad.net/connected", shell=True, stdout=subprocess.PIPE).stdout
    results = proxycheck.read()
    if "You are connected to Mullvad" in str(results):
        return True


def remediate():
    os.system("systemctl restart mullvad*")
    time.sleep(10)
    if check_mullvad():
        log_fixed()
        exit()
    else:
        log_failure()
        os.system("systemctl stop " + restart_me)


def log_fixed():
    os.system("logger -p 'user.crit' 'Mullvad crashed, restart successful.'")


def log_failure():
    os.system("logger -p 'user.crit' 'Mullvad failed to restart. Stopping ' + restart_me")

def log_good():
    os.system("logger 'Ran proxy checking script. No problems detected.'")


if __name__ == '__main__':
    if check_mullvad():
        log_good()
        exit()
    else:
        print(check_mullvad())
        remediate()