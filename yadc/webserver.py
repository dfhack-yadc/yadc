import json
import os
import sys

try:
    import bottle
except ImportError:
    print('bottle not found. This is most likely due to running webserver.py directly.\n'
          'main.py should be used instead')
    sys.exit(1)
from bottle import redirect, request, response, route, static_file, view

import yadc.util as util

bottle.TEMPLATE_PATH.append(util.abspath('remote/templates'))

g_data = dict()

# from http://bottlepy.org/docs/dev/recipes.html#ignore-trailing-slashes
class StripTrailingSlashMiddleware(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.app(e, h)

@route('/game')
@view('game_list')
def callback():
    return dict()

@route('/static/<path:path>')
def callback(path):
    return static_file(path, util.abspath('static'))

@route('/yadc/ports.js')
def callback():
    response.content_type = 'text/javascript'
    return 'YADC_PORTS = %s;' % json.dumps({
        k: g_data.get(k, -1) for k in ('web_server_port', 'comm_server_port', 'screen_server_port')
    })

def define_redirect(old_url, new_url):
    @route(old_url)
    def callback():
        redirect(new_url)

define_redirect('/', '/game/')
define_redirect('/static', '/static/index.html')

def main(addr, port, data=None):
    try:
        addr, port = str(addr), int(port)
    except ValueError:
        raise ValueError('Invalid server address: %s:%s' % (addr, port))
    if isinstance(data, dict):
        global g_data
        g_data = data
    try:
        app = bottle.app()
        app = StripTrailingSlashMiddleware(app)
        bottle.run(app=app, host=addr, port=port,
                   debug=bool(os.environ.get('YADC_DEBUG', False)))
    except Exception as e:
        raise Exception('Web server error: %s' % e)
