#! /usr/bin/env python

import os
import subprocess
import sys

import yadc.comm
import yadc.util
from yadc.util import abspath, printl

# Add ./depends to path
if not os.path.isdir('depends'):
    os.mkdir('depends')
sys.path.insert(sys.path.index('') if '' in sys.path else 0, abspath('depends'))
from yadc.check_env import check_env
if not check_env():
    print('\nEnvironment check failed!')
    sys.exit(1)
else:
    print('yadc: Environment check successful')

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
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
