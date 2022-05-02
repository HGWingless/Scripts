# 20220501 - v1.0 - Exports chunks of video from the CLI on Unifi devices. Run the program to see required args.
# DEPENDS ON convert_local_time script.
# This has only been tested on Cloudkey 2, so YMMV may vary with other solutions.
import datetime
import os
import convert_local_time
import argparse
import re


def get_path(some_date):
    """Assembles the path to where the video files are stored, based on the date a user wants to export"""
    date_split = some_date.split('-')
    base_path = '/srv/unifi-protect/video/' + date_split[0] + '/' + date_split[1] + '/' + date_split[2] + '/'
    return base_path


def get_export_list(user_dir, f, t, mac):
    """Given a directory path, from and to hours, and the MAC, filter the video files we need to export
    Returns a list"""
    results = []
    final_list = []
    # For high quality video files, if the local recording time for a file is within the high and low hour limits
    # Add it to a list. Then return a list that is filtered by MAC.
    for i in user_dir:
        epoch = re.search(".*0_rotating_(.*).ubv", i)
        try:
            local_time = datetime.datetime.fromtimestamp(int(epoch.group(1)) / 1000)
            time_re = re.search('.* (\d\d)', str(local_time))
            if int(f) <= int(time_re.group(1)) <= int(t):
                results.append(i)
        except:  # Exceptions are non-matching files. Ignore them
            pass
    for a in results:
        if mac in a:
            print(a + ' is a match, adding to export.')
            final_list.append(a)
    return final_list


def run_export(final):
    """Build the parameters to pass to Unifi's export binary and run it"""
    # Each file to be included in export needs to be a -s parameter, in order
    dash_ess = '-s ' + ' -s '.join(final)
    command = UNIFI_EXPORT_BIN + ' ' + dash_ess + ' -d ' + outfile_loc + '/'
    os.system(command)


if __name__ == '__main__':
    # Create parser (argparse). All of these are mandatory, and no error checking is done, so I'm leaving them global.
    parser = argparse.ArgumentParser()
    # Add arguments
    parser.add_argument('-d', '--date', type=str, required=True,
                        help='The date to export from in YYYY-MM-DD format')
    parser.add_argument('-f', '--fromhour', type=str, required=True,
                        help='The HOUR you want to start exporting from')
    parser.add_argument('-t', '--tohour', type=str, required=True, help='The HOUR you want to stop exporting from')
    parser.add_argument('-o', '--outfile', type=str, required=True,
                        help='The path to export the finished MP4s to. Should be on external storage for managed '
                             'systems. No trailing slashes, or you will probably end up writing to root.')
    parser.add_argument('-m', '--mac', type=str, required=True,
                        help='The MAC of the device you want to export. No hyphens')

    # Parse arguments
    args = parser.parse_args()
    from_hour = int(args.fromhour)
    to_hour = int(args.tohour)
    mac_address = str(args.mac)
    outfile_loc = str(args.outfile)
    args_date = str(args.date)
    #############################################
    # Location of the binary that actually exports the video files
    UNIFI_EXPORT_BIN = '/usr/share/unifi-protect/app/node_modules/.bin/ubnt_ubvexport'

    date_path = get_path(args_date)  # Build the file path given a date
    dir_list = convert_local_time.get_dirlist(str(date_path))  # Get list of video files
    # Get a list of files filtered by provided time and MAC address
    final_list = get_export_list(dir_list, from_hour, to_hour, mac_address)
    run_export(final_list)
