#!/usr/bin/env python

import subprocess, sys, json
import datetime

__author__ = "imad abdou"

BACKUP_REMOTE = 'lexup1:'
CONTAINER_NAME = 'etmsd8'

# main lxd entry point
def main():
    NAME = '"lexup_{0:%Y-%m-%d-%H:%M}"'.format(datetime.datetime.now())
    subprocess.call(['lxc', 'stop', CONTAINER_NAME])
    publish_lxd(NAME)


def publish_lxd():
    print('[lexup] publishing {} to remote: {}, please wait...'.format(CONTAINER_NAME, BACKUP_REMOTE))
    success = subprocess.call(['lxc', 'publish', CONTAINER_NAME, BACKUP_REMOTE, '--alias', NAME])

    if(success == 0):
        print('[lexup] container backup completed!, image name: {}'.format(NAME))
    else:
        print('[lexup] error, backup proccess did not complete')
    subprocess.call(['lxc', 'start', CONTAINER_NAME])


if __name__ == "__main__":
    main()