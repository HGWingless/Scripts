# REQUIRES POWERCLI
# 20220420 - This script pulls the annotations(notes) for machines in a specific folder. 
# For example, if you move decomissioned servers to a folder until you're sure they can be purged, this script will give 
# you the notes fields from those servers.
# CUSTOMIZE THESE VARIABLES TO MATCH YOUR ENVIRONMENT
$outfile = "old_export.csv"
$vmware_server = "YOURSERVER.COM"
# END CUSTOMIZATION

connect-viserver $vmware_server
# Get the names of every VM in the old folder
$vms = get-folder "Old" | get-vm | Select-Object -ExpandProperty Name
# For each vm name, get the name and notes and put it in an object.
foreach ($line in $vms) {
    $infotemp = [PSCustomObject]@{
        Name = (get-vm $line).Name
        Notes = (get-vm $line).Notes
        
    }
    # Output that object to console. Uncomment CSV line if you want an export
    $infotemp
    $infotemp | Export-Csv $outfile -Append
    
disconnect-viserver -confirm:$false
} 