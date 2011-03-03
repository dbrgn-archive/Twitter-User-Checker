#!/usr/bin/env python2

# Twitter User Checker
# Author: Danilo Bargen
# License: GPLv3

import sys
import urllib2
import json
from datetime import datetime, timedelta
import math

try:
    user = sys.argv[1]
except IndexError:
    print 'Usage: checkuser.py [username]'
    sys.exit(-1)

url = 'http://api.twitter.com/1/users/show.json?id=%s' % user

try:
    request = urllib2.urlopen(url)
    status = request.getcode()
    data = request.read()
except urllib2.HTTPError as e:
    status = e.getcode()
    data = e.read()

data = json.loads(data)

if status == 403:
    if 'suspended' in data['error']:
        print 'User %s has been suspended' % user
    else:
        print 'Unknown response'
elif status == 404:
    print 'User %s not found' % user
elif status == 200:
    seconds_active = (datetime.now() - datetime.strptime(data['created_at'],
                   '%a %b %d %H:%M:%S +0000 %Y')).total_seconds()
    days_active = int(math.ceil(seconds_active / 3600 / 24))
    print 'User %s is active and has posted %s tweets in %s days' % \
             (user, data['statuses_count'], days_active)
else:
    print 'Unknown response'
