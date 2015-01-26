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
        'web_server_port': int(os.environ.get('YADC_WEB_SERVER_PORT', -1)),
        'comm_server_port': int(os.environ.get('YADC_COMM_SERVER_PORT', -1)),
        'screen_server_port': int(os.environ.get('YADC_SCREEN_SERVER_PORT', -1)),
    })

def define_redirect(old_url, new_url):
    @route(old_url)
    def callback():
        redirect(new_url)

define_redirect('/', '/game/')
define_redirect('/static', '/static/index.html')

def main():
    try:
        addr, port = sys.argv[1], int(sys.argv[2])
    except (TypeError, ValueError) as e:
        util.err('Invalid server address: ' + sys.argv[1])
        return
    try:
        app = bottle.app()
        app = StripTrailingSlashMiddleware(app)
        bottle.run(app=app, host=addr, port=port,
                   debug=bool(os.environ.get('YADC_DEBUG', False)))
    except Exception as e:
        util.err('Web server error: %s' % e)
        return

if __name__ == '__main__':
    main()
