import os
import sys

import bottle
from bottle import request, route, static_file

import yadc.util as util

@route('/static/<path:path>')
def callback(path):
    return static_file(path, util.abspath('static'))

def main():
    try:
        addr, port = sys.argv[1], int(sys.argv[2])
    except (TypeError, ValueError) as e:
        util.err('Invalid server address: ' + sys.argv[1])
        return
    try:
        bottle.run(host=addr, port=port, debug=bool(os.environ.get('YADC_DEBUG', False)))
    except Exception as e:
        util.err('Web server error: %s' % e)
        return

if __name__ == '__main__':
    main()
