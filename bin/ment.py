#!/usr/bin/python3

import sys, re, fileinput
import glob, fnmatch, os, os.path, tempfile, shutil
import time, datetime, sqlite3, json

from boot import api

from TwitterAPI import TwitterRestPager as TP

endpoint = 'statuses/mentions_timeline'
params   = {'count' : 200, 'trim_user': 1}
pager    = TP(api, endpoint, params )

users = set()

for tweet in pager.get_iterator():
    users.add(tweet['user']['id_str']) # or id as int

users = list(users)

endpoint = 'lists/members/create_all'
params = {'slug': 'Summer', 'owner_screen_name': 'shuravban', 'user_id': ""}

# only 100 users by time
MAX=100
n = len(users)//MAX + 1
for i in range(n):
    params['user_id'] = ", ".join(users[i*MAX : i*MAX+MAX])
    res = api.request(endpoint, params)
    if res.status_code != 200:
        raise Exception # TODO

print('DONE')
