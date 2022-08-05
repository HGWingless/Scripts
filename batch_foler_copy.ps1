# This script iterates through a file of users and builds src/dst paths to use in robocopy. 
# In short, copy a specific list of folders from one place to another.
# --------------- Instructions
# Edit the path to the CSV file and the name of the column to get our target directories
# Edit the from and to vars to set the base directory to build names from
# Edit the switches variable to customize run parameters

# Path to CSV to import
$csv_path = '.\test.csv'
# Column in the CSV to build paths from
$column_name = 'name'
#Root path to where we're copying
$from = '\\myserver\share\'
$to = '\\newserver\share\'
# List of switches to run. 
# Defaults to subdirectory and security copy, with continue, excluding junctions. Exclude trash files and set retry/limits, with 16 threads
# Consider adding /L to dry-run before kicking off this whole batch
$switches = '/E /SEC /Z /xjd /R:2 /W:1 /XF "*.db" "*.ds" "*.tmp" "*DS_Store*" "*.done" ".*" ".$" /MT:16'
#Import CSV
$data = Import-Csv $csv_path -Delimiter ","
#For each row, take the name column and cat it w/ the destination
foreach($row in $data){
    $catfrom = $from + $row.$column_name
    $catto = $to + $row.$column_name
    # Excludes some junk files (dotfiles, temp, thumb dbs) and use 16 threads, short wait/skip periods
    $runthis = 'robocopy.exe ' + $catfrom + ' ' + $catto + ' ' + $switches
    Invoke-Expression -Command $runthis
}
