#! /usr/bin/env python

from __future__ import print_function

import json
import os
import socket
import subprocess
import sys
import textwrap
import time
import traceback

import yadc
from yadc.util import abspath, printl

os.chdir(os.path.dirname(os.path.abspath(__file__)))
yadc.util.update_path()
from yadc.check_env import check_env
if not check_env():
    print('\nEnvironment check failed!')
    sys.exit(1)
else:
    print('yadc: Environment check successful')

def test_port(port, silent=False):
    write = (lambda s: None) if silent else printl
    tries = 0
    while True:
        try:
            # Wait for port to become available
            # connect_ex() may be better suited for this purpose, but it's
            # possible for a "killed" Django server to appear responsive
            # for some time after it is killed
            sock = socket.socket()
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('0.0.0.0', port))
            sock.close()
        except socket.error as e:
            if tries == 0:
                write("""
Port %i appears to be in use. This can happen if the server was recently killed,
for instance. yadc will attempt to wait for this port to become available.

To use another port, stop this process (e.g. with Ctrl-C) and edit yadc.json in
this folder.

""" % port)
                write('Scanning')
            write('.')
            tries += 1
            if tries >= 30:
                write('\nTimed out after %i seconds: %s\n' % (tries, e))
                raise IOError('Unable to bind to port %i' % port)
            time.sleep(1)
        else:
            if tries:
                write('\nPort %i now available\n' % port)
            break

def main():
    config = yadc.config.Config()
    try:
        config.load('yadc.json')
    except IOError:
        print('Failed to read from yadc.json')
    except ValueError:
        print('yadc.json is malformed')
        return
    web_server_port = config.get('web_server_port', 8000)
    comm_server_port = config.get('comm_server_port', 25143)
    screen_server_port = config.get('screen_server_port', 25144)
    web_server_process = None
    try:
        test_port(web_server_port)
        test_port(comm_server_port)
        test_port(screen_server_port)
    except IOError:
        traceback.print_exc()
        return False
    try:
        # TODO: Only run this when necessary
        subprocess.call(['python', abspath('yadc_remote/manage.py'), 'migrate'])
        comm_server = yadc.comm.CommServer(port=comm_server_port)
        screen_server = yadc.comm.ScreenServer(port=screen_server_port)
        web_server_env = os.environ.copy()
        web_server_env['PYTHONPATH'] = ':'.join(sys.path)
        web_server_process = subprocess.Popen([
                sys.executable,
                abspath('yadc_remote/manage.py'), 'runserver',
                '0.0.0.0:%s' % str(web_server_port)
            ],
            env=web_server_env,
            shell=False
        )
        comm_server.listen()
        screen_server.listen()
        web_server_process.wait()
    except KeyboardInterrupt:
        print('\n')
        try:
            comm_server.shutdown()
        except socket.error:
            print('Failed to shut down server: %r' % comm_server)
        try:
            screen_server.shutdown()
        except socket.error:
            print('Failed to shut down server: %r' % screen_server)
    except Exception as e:
        traceback.print_exc()
    if web_server_process:
        printl('Stopping web server... ')
        try:
            web_server_process.terminate()
        except Exception as e:
            print('Failed: %s' % e)
        else:
            print('Ok')

if __name__ == '__main__':
    main()
