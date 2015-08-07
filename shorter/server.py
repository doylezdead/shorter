import subprocess as sp
import os
import signal
import sys

import bottle

import shorter.shorter_db as cdb


def interrupt_handler(signal, frame):
    print('shutting down mongod...')
    mongo_proc.send_signal(15)
    print('shutting down cpunch server...')
    sys.exit(0)

os.makedirs(os.path.expanduser('~/.shorter/db'), exist_ok=True)
mongo_args = ['mongod', '--logpath', os.path.expanduser('~/.shorter/mongolog'), '--bind_ip',
              '127.0.0.1', '--port', '25252', '--dbpath', os.path.expanduser('~/.shorter/db')]
mongo_proc = sp.Popen(mongo_args)
signal.signal(signal.SIGINT, interrupt_handler)

dbuser = cdb.DBUser(port=25252)         # create a new dbuser instance to start handling the data package

@bottle.route('/reg/<url>', method='GET')
def reg(url):
    retkey = dbuser.register_url(url)
    return retkey


@bottle.route('/<key:re:([a-z]|[A-Z]|[0-9]){6}>')
def resolve(key):
    returl = dbuser.resolve_key(key)
    return returl


print('Ctrl-C to gracefully shut down server')
bottle.run(host='0.0.0.0', port=5000)
