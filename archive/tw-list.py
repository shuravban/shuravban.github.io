#!/usr/bin/python3

import sys, re, fileinput
import glob, fnmatch, os, os.path, tempfile, shutil
import time, datetime, sqlite3, json
import argparse

from boot import api

from TwitterAPI import TwitterRestPager as TP

PROGNAME = os.path.basename(__file__)

def usage(status=0):
    print('''
Usage: %s [-u|--user USER] LIST
Print user ids from LIST
''' % PROGNAME)

def whoami():
    res = api.request('account/settings')
    return res.json()['screen_name']

def ids(user, slug):
# count may be 5000 - and members in list 5000 - iteration isn't needed
# slug - "Хорошие-люди"
    endpoint='lists/members'
    params={'count': 5000, 'owner_screen_name':user, 'slug':slug}
    res = api.request(endpoint, params)
    rst = list(map(lambda x: x['id_str'], res.get_iterator()))
    return rst

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Print ids from LIST')
    parser.add_argument(
        '-u', '--user',
        metavar='USER',
        type=str,
        help='Screen name of the owner of the LIST',
    )
    parser.add_argument(
        'slug',
        metavar='LIST',
        type=str,
        help='Name(slug) of the LIST',
    )
    args = parser.parse_args()

    user = args.user
    if not user:
        user = whoami()

    print("\n".join(ids(user, args.slug)))
