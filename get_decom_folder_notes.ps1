# Connect to vcenter and pull a list of machines in your decommission folder (or whatever folder)
# Export names and notes (or whatever else you want to pull from the object) and export to a csv. Disconnect.
$outfile = "old_export.csv"
# ---Put vcenter server name here!---
$vmware_server = ""
# Folder you want to pull all machines from
$decom_folder = "Old"

connect-viserver $vmware_server
# Get the names of every VM in the old folder
$vms = get-folder $decom_folder | get-vm | Select-Object -ExpandProperty Name
# For each vm name, get the name and notes and put it in an object.
foreach ($line in $vms) {
    $infotemp = [PSCustomObject]@{
        Name = (get-vm $line).Name
        Notes = (get-vm $line).Notes
        
    }
    # Output that object to console. Export to CSV
    $infotemp
    $infotemp | Export-Csv $outfile -Append
    
} 
disconnect-viserver -confirm:$false