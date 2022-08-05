# For a given search base, get all DNS names for AD objects and run a connection test. 
# All objects that fail test are written to an output file
# Errors are suppressed. Search base should be quoted if entered as param, and not quoted if input via readline
param(
    [string]$Base = $(Read-Host "What is the search base (OU=,DC=, etc.)?"))

# Get a list of computer objects from the given search base. Store DNS name
$server_hosts = Get-ADComputer -SearchBase "$Base" -Filter * | select dnshostname -ExpandProperty dnshostname
# For every computer in the variable, run a test connection. Computers that fail get put in a file on the desktop
foreach ($computer in $server_hosts){
    $results = Test-Connection $computer -count 1 -erroraction Ignore
    if (($results -eq "") -or ($results -eq $null)) {$computer | Out-File ~\Desktop\tc_all_servers.txt -Append}}