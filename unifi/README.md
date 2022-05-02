# Unifi Video Time Converter and Exporter

These scripts make working with larger exports, and exporting on the CLI a little easier to work with, or use this in a cron job to export specific times. These scripts were written for a Cloudkey 2, so your mileage may vary on other platforms if the paths differ, but hopefully a path change (or a code snippet from someone) will get it working.

Copy/clone both scripts onto your NVR/cloudkey, chmod +x them to make them executable and run them from there.


# Files

**convert_local_time** - If you browse the file structure on your controller, video files are listed by date, and then by blocks of time which are separated by whatever would make that video blob be 1GB. The timestamps in the file are written in Unix time, so this script converts those times to local time so you can be better prepared for an export, be it manual through Unifi's export binary, or in lazy, scripted bulk using the other script. Note that the timestamp is when the file STARTS. 

Takes exactly one argument (date to query). Example: **./convert_local_time.py 20220501**

Example output:

    

> 2022-04-22 10:57:58.281000 --> MYMAC_0_rotating_1650650278281.ubv
2022-04-22 13:43:43.246000 --> MYMAC_0_rotating_1650660223246.ubv
2022-04-22 16:26:59.146000 --> MYMAC_0_rotating_1650670019146.ubv
2022-04-22 19:14:13.180000 --> MYMAC_0_rotating_1650680053180.ubv
2022-04-22 22:04:33.124000 --> MYMAC_0_rotating_1650690273124.ubv
---

**export_video** - This acts as a wrapper for Unifi's video export binary. This lets a user export for a time range without manually converting Unix time or assuming based on last modified times.  The user passes a date, hour range arguments, an output file and MAC to filter on and an export is started. Consider that since the timestamps in the name are for when the section STARTS, you might want to move your start time back an extra hour if you think you might miss some relevant bits. Use convert_local_time to check what the difference between the last section of the previous hour and the first section of your start hour is to make a more informed decision.

## Flags 
All arguments are required
*-d* Date in YYYY-MM-DD format
*-f* Start hour
*-t* End hour
*-o* output file root location (no trailing slashes)
*-m* the MAC address to filter on. (You can check your device MACs in Protect > Devices)

Sample output:
>MYMAC_0_rotating_1650658808145.ubv is a match, adding to export.
MYMAC_0_rotating_1650660313158.ubv is a match, adding to export.
MYMAC_0_rotating_1650661749315.ubv is a match, adding to export.
MYMAC_0_rotating_1650663339176.ubv is a match, adding to export.
MYMAC_0_rotating_1650665893292.ubv is a match, adding to export.
Creating file /mnt/_0.mp4 starting at 2022-04-22T20:19:52.354

Example for exporting start hours 13 through 15 on 2022-04-22 and outputting to /mnt:

**export_video.py -d 2022-04-22 -f 13 -t 15 -o /mnt -m 123456ABCD55**
