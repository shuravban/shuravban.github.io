#!/usr/bin/python3

import sys, re, fileinput
import glob, fnmatch, os, os.path, tempfile, shutil
import time, datetime, sqlite3, json

from boot import api

PROGNAME = os.path.basename(__file__)

def usage(status=0):
    print("Usage: %s [SCREEN_NAME]" % PROGNAME)
    sys.exit(status)

def get_ids(screen_name):
    endpoint = 'followers/ids'
    params = {'cursor': -1}
    if screen_name:
        params['screen_name'] = screen_name
    while True:
        res = api.request(endpoint, params)
        for id in res.get_iterator():
            print(id)
        next_cursor = res.json()['next_cursor']
        if next_cursor == 0:
            break
        params['cursor'] = next_cursor


if __name__ == '__main__':
    if len(sys.argv) > 2:
        usage(1)

    arg = ""
    if len(sys.argv) == 2:
        arg = sys.argv[1]

    if arg == '-h' or arg == '--help':
        usage()

    get_ids(arg)
