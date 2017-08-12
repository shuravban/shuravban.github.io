#!/usr/bin/python3

import sys, re, fileinput
import glob, fnmatch, os, os.path, tempfile, shutil
import time, datetime, sqlite3, json

from boot import api

from TwitterAPI import TwitterRestPager as TP

PROGNAME = os.path.basename(__file__)

def usage(status=0):
    print('''
Usage: %s LIST
Ger user ids from stdin ant put them on the LIST
''' % PROGNAME)

def whoami():
    res = api.request('account/settings')
    return res.json()['screen_name']

def list_add(list, ids):
    endpoint = 'lists/members/create_all'
    user = whoami()
    params = {'slug' = list, 'owner_screen_name' = user }

    m = 100
    n = len(ids)//m + 1
    for i in range(n):
        params['user_id'] = ",".join(ids[i*m:i*m+m])
        api.request(endpoint, params)


if __name__ == '__main__':
    if len(sys.argv) !=2:
        usage(1)

    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        usage(0)

    ids = []
    for line in sys.stdin.readlines():
        ids += line.split()

    list_add(sys.argv[1], ids)
