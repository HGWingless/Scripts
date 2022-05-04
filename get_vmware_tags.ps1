# REQUIRES VMWARE POWERCLI
# 20220413 - This script takes a text file of servers, and returns the email addresses of the individuals on the notify list
# for those servers. This assumes your notify tags are as such to where notify+domain will be an email address
# UPDATE THESE VARIABLES TO MATCH YOUR ENVIRONMENT
$in_file = "./notify_list.txt" # Where the list of servers lives
$vmware_server = "" # YOUR VCENTER SERVER
$email_domain = 'whatever.com'
# Connect to vcenter. 
connect-viserver $vmware_server # THIS ASSUMES YOU HAVE CREDS STASHED VIA POWERCLI, OR YOUR ACCOUNT HAS PERMISSIONS TO TAKE THESE ACTIONS
### End customization

# For each line in the server list, pull the VM's tags, return only the UID of people to notify based on associated notify tags
# Runs a uniq on them to keep the list concise .
foreach($line in Get-Content $in_file) {
    $list += (Get-TagAssignment $line).Tag | where Category -like 'Notify' | select Name -ExpandProperty Name 
    $list += ' '
    $list_array = $list.Split() | Sort-Object | Get-Unique    
}
# Appends $email_domain for easier copy/paste to email (as long as the evaulated line isn't blank)
foreach($line in $list_array) {
    if ($line -ne '') {
        $to_address += $line += $email_domain + '`n'
        
    }
}

# Text output, giving servers to reboot and whom to notify for easy copy-paste into an email
$output = Write-Output "For the following servers to be rebooted:`n"
$output += Get-Content $in_file | Out-String
$output += Write-Output "`nThese people should be notified:`n`n"
$output += $to_address
$output

# Clears variables to prevent bad data if run repeatedly with different input
Clear-Variable -Name "list_array"
Clear-Variable -Name "list"
Clear-Variable -Name "to_address"