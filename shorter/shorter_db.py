__author__ = 'rcdoyle'

import pymongo
import time
import random
import string

class DBUser:

    def __init__(self, port=25252):
        self.client = pymongo.MongoClient('localhost', port)
        self.authenticated = False

    def register_url(self, url):
        rand = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for i in range(6))

        col = self.client['routes']['pairs']

        col.insert_one({
            'timestamp': time.time(),
            'key': rand,
            'url': url
        })
        return rand

    def resolve_key(self, key):
        col = self.client['routes']['pairs']
        matches = col.find({'key': key})

        url = 'http://breadfish.co.uk'
        for x in matches:
            url = x['url']
            break
        return url
