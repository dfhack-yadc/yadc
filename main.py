#! /usr/bin/env python

import os
import subprocess
import sys

import yadc.comm

def abspath(path):
    return os.path.join(os.getcwd(), *path.split('/'))

def printl(*args):
    sys.stdout.write(*args)
    sys.stdout.flush()

# Add ./depends to path
sys.path.insert(sys.path.index('') if '' in sys.path else 0, abspath('depends'))
from yadc.check_env import check_env
if not check_env():
    print('\nEnvironment check failed!')
    sys.exit(1)

def main():
    web_server_process = None
    try:
        comm_server = yadc.comm.CommServer(25143)
        screen_server = yadc.comm.ScreenServer(25144)
        web_server_env = os.environ.copy()
        web_server_env['PYTHONPATH'] = ':'.join(sys.path)
        web_server_process = subprocess.Popen(['python', abspath('yadc_remote/manage.py'), 'runserver'], env=web_server_env)
        web_server_process.wait()
    except KeyboardInterrupt:
        print('\n')
    except Exception as e:
        print('\nError: %s' % e)
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
