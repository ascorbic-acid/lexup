a simple python3 script that use **lxc export** to backup lxd containers

what the script does:
- delete old backups which exceeds X days (can be disabled)
- backup one or more containers one by one
- option to backup with or without shutting containers down
- store backups to a selected folder (created automatically if not exist)

