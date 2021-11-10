#!/usr/bin/python3
import datetime
import os
import subprocess
import tempfile
import shutil
from dateutil.parser import parse


# Container names which you want to backup
BACKUP_CONTAINERS = ["ubu", "wow"]

# Path where you want store the backups
BACKUP_FOLDER  = "/home/imad/Documents/lxd-backups"

# Delete the backups which are older than X days
# Set to 0 to disable
BACKUP_VALIDITY_DAYS = 30

# Shutdown the container before backup (might be a bit faster and safer)
SHUTDOWN_BEFORE_BACKUP = True

def main():
    # create the backup folder if not exist
    if not os.path.exists(BACKUP_FOLDER):
        os.mkdir(BACKUP_FOLDER)

    # remove old backups
    if BACKUP_VALIDITY_DAYS > 0:
        old_backup_files = os.listdir(BACKUP_FOLDER)

        for backup_name in old_backup_files:
            backup_date = parse(backup_name, fuzzy=True)

            if (datetime.datetime.now() - backup_date).days > BACKUP_VALIDITY_DAYS:
                backup_path = os.path.join(BACKUP_FOLDER, backup_name)
                os.remove(backup_path)
                print(f"Backup: {backup_name} exceeded the validity days ({BACKUP_VALIDITY_DAYS} Day) and got Deleted.")

    # Backup the target containers
    tmp_folder = tempfile.TemporaryDirectory()
    for container in BACKUP_CONTAINERS:
        backup_file_name = f"{container}-{datetime.datetime.now().strftime('%Y-%m-%d:%H:%M')}.tar.gz"
        full_backup_file_path = os.path.join(tmp_folder.name, backup_file_name)
        
        try:
            if SHUTDOWN_BEFORE_BACKUP:
                print(f"Shutting down Container: {container}...")
                subprocess.call(["lxc", "stop", container])

            print(f"Backing up Container: {container}...")
            subprocess.check_call(["lxc", "export", container, full_backup_file_path])

        except subprocess.CalledProcessError as e:
                print(e.output)
        finally:
            print(f"Starting up Container: {container}...")
            subprocess.call(["lxc", "start", container])

        # move the backup file from tmp to the backup folder
        if os.path.exists(full_backup_file_path):
            final_path = shutil.move(full_backup_file_path, BACKUP_FOLDER)
            print(f"Container {container} stored at: {final_path}\n")



if __name__ == '__main__':
    main()
