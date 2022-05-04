# This script will return the local administrator group members for computer objects, starting with a base directory. This requires some customization of variables below, or it will not run.
# 20220316 - v1 commit.
# Concatonate a list of Windows servers, including domain controllers to run script against
# You will want to update these variable to match your environment (search pattern, output path, mail recipients)
# Due to naming convention, this gets all servers in a base OU, and excludes linux servers (by name with wildcard*). Probably different in your environment, so customize the search
$vms1 = get-adcomputer -filter * -searchbase "ou=servers,ou=,dc=,dc=,dc=" -Properties * | ? distinguishedname -NotLike "*linux*" | select name | sort name
# Add any other servers you want to include, or blank out this string if unused
$vms2 =  'someotherserver'
$vms3 = $vms1.name + $vms2
$currentpath = 'c:\local_admins.csv' # Path of file with current run's results
$oldpath = 'c:\local_admins_last.csv' # Path of file with the previous run's results
$compare = ''
# To/from/smtp information
$EmailSender = ''
$EmailRecivers = @('')
$smtpserver = ''

# Variables for environment ends. Actual code begins


# See if a report exists already from a previous run. If it does, rename to oldpath variable
if (Test-Path -Path $currentpath -PathType Leaf) {
    Remove-Item -Path $oldpath
    Rename-Item -Path $currentpath -NewName $oldpath
}

# For each computer in $vms3, get the local group 'Administrators', names only. Create a new psobject with computer name, group, and members
Invoke-Command -computername $vms3 {
    $members = Get-LocalGroupMember -Group "Administrators" | Select-Object name -ExpandProperty name 
    New-Object PSObject -Property @{
    Computername = $env:COMPUTERNAME
    Group = "Administrators"
    Members = $members
    }
} | # Select all objects and dump into a csv. Excludes for brevity
    Select-Object * -ExcludeProperty RunspaceID | Export-Csv $currentpath -NoTypeInformation

# If there is a file from a previous run, compare that run to this run, create a diff, and email the csvs.    
if (Test-Path -Path $oldpath -PathType Leaf) {
    $compare = Compare-Object $(Get-Content $currentpath) $(Get-Content $oldpath) -IncludeEqual
    $compare
    $body = "Diff of CURRENT vs LAST week's admin list" + "`n" + ($compare | Out-String)
    $Body = $Body | Out-String
    Send-MailMessage -from $EmailSender -to $EmailRecivers -Subject 'Local Admin Report' -SmtpServer $smtpserver -body $Body -Attachments $currentpath
} else { # Otherwise, just send out this run's csv
    $body = "Current week's admin list"
    $body += "`n"
    $Body = $Body | Out-String
    Send-MailMessage -from $EmailSender -to $EmailRecivers -Subject 'Local Admin Report' -SmtpServer $smtpserver -body $Body -Attachments $currentpath   
}