# 20220501 - v1.0 - Prints out local times (instead of Unix) for Unifi Protect videos, given a date
# This has only been tested on Cloudkey 2, so YMMV may vary with other solutions.
import fnmatch
import os
import sys
import re
import datetime


def validate():
    """If the user didn't supply the right # of arguments, give help and exit. """
    if len(sys.argv[1:]) != 1:
        error_close()
    else:
        return sys.argv[1]


def error_close():
    """" This prints help text and exits"""
    print(
        "If you are running this directly, you must supply exactly one argument, the directory path you are converting"
        "time for.")
    exit()


def get_path(some_date):
    """Assembles the path to where the video files are stored, based on the date a user wants to export"""
    date_split = some_date.split('-')
    base_path = '/srv/unifi-protect/video/' + date_split[0] + '/' + date_split[1] + '/' + date_split[2] + '/'
    return base_path


def get_dirlist(passed_dir):
    """Takes all ubv files in a given directory and returns a sorted list"""
    file_list = os.listdir(passed_dir)
    EXT_FILTER = '*.ubv'
    ext_matches = []
    for i in file_list:
        if fnmatch.fnmatch(i, EXT_FILTER):
            ext_matches.append(i)
    ext_matches.sort()
    return ext_matches


def get_time(files):
    """For all high quality videos, convert the Unix time in the file name to local times. Print results"""
    for f in files:
        epoch = re.search(".*0_rotating_(.*).ubv", f)
        try:
            local_time = datetime.datetime.fromtimestamp(int(epoch.group(1)) / 1000)
            print(str(local_time) + ' --> ' + str(f))
        except:
            pass


if __name__ == '__main__':
    user_date = validate()  # Make sure we have an argument
    parsed_path = get_path(user_date)  # Build a path based on given date
    list_of_files = get_dirlist(parsed_path)  # Create a list of video files in that directory
    get_time(list_of_files)  # Convert to local time and print
