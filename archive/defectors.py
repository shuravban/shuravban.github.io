#!/usr/bin/python3

import sys, re, fileinput
import glob, fnmatch, os, os.path, tempfile, shutil
import time, datetime, sqlite3, json

import tweepy

from boot import api

lst = 'defectors'

# Twitter API - GET friends/ids - 5000 15x15
c = tweepy.Cursor(api.friends_ids)
friends = set(c.items())

# -- // --
c = tweepy.Cursor(api.followers_ids)
followers = set(c.items())

# After notes - из абстракции только курсор и он сработал - не
# нужно было вручную отслеживать. А так - прямое отображение

current_rats = friends - followers

# maximum 5000
# rats = api.list_members('shuravban', 'defectors')

for rat in current_rats:
    api.add_list_member(owner_screen_name='shuravban', slug=lst, user_id=rat)

# That's all, folks
