#!/usr/bin/python

from __future__ import print_function

# gistquery is a utility to query a single user's GitHub gists
#
# Syntax:
#
# gistquery <username>
#
# Where <username> is the Github user's username.
#
# The first time you query a user's gist it will register the current
# gists for that user and show the date of the latest gist. The user
# will be registered in a file named "/tmp/gistquery.<username>". Subsequent
# executions for the same username will tell
# you if a new gist has been added by the user.

import os
import argparse
try:
    import simplejson as json
except ImportError:
    import json
from datetime import datetime
import urllib
import requests

# Parse command line arguments

parser = argparse.ArgumentParser()
parser.add_argument("gitUser", help="Github username for gists query")
args = parser.parse_args()
GIST_URL = 'http://api.github.com/users/' + args.gitUser + '/gists'

# Attempt to connect to Github and query user's Gists
# If status code is not 200 handle it and exit

r = requests.get(GIST_URL)
if r.status_code <> 200:
    if r.status_code == 404:
        print ('Error: Github user "' + args.gitUser + '" not found.')
    else:
        r.raise_for_status()
    exit(255)
gist = json.loads(r.content)
if not gist:
    print ('Github user "' + args.gitUser + '" has not published any gists.')
    exit(1)

# At this point we have a user who has public gists. We now need to check
# if there is a previous record of a query. If not, this is a new record
# that needs to be created. Otherwise we read the record file to get the
# date of the last check, compare against the latest gist and notify if
# the user has created a new gist.

configPath = '/tmp/gistquery.' + args.gitUser
if not os.path.isfile(configPath):
    print('Github user "' + args.gitUser +
        '" gists have not been previously queried.')
    print('Creating checkpoint file: ' + configPath)
    try:
        configFile = open(configPath, "w")
        configFile.write(gist[0]['created_at'])
        configFile.close()
    except Exception as e:
        raise
else:
    try:
        configFile = open(configPath,"rw")
        stringDate = configFile.read()
    except Exception as e:
        raise
    lastCreateDate = datetime.strptime(stringDate,'%Y-%m-%dT%H:%M:%SZ')
    currentLastCreateDate = datetime.strptime(gist[0]['created_at'],
        '%Y-%m-%dT%H:%M:%SZ')
    if currentLastCreateDate > lastCreateDate:
        print('Github user "' + args.gitUser +
            '" created a new gist since the last query.')
        try:
            configFile.seek(0,0)
            configFile.write(gist[0]['created_at'])
        except Exception as e:
            raise
    else:
        print('Github user "' + args.gitUser +
            '" has not created a new gist since the last query.')
    configFile.close()
exit(0)
