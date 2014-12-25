#! /usr/bin/env python

import json
import os
import subprocess
import sys

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
    web_server_process = None
    try:
        # TODO: Only run this when necessary
        subprocess.call(['python', abspath('yadc_remote/manage.py'), 'migrate'])
        comm_server = yadc.comm.CommServer(25143)
        screen_server = yadc.comm.ScreenServer(25144)
        web_server_env = os.environ.copy()
        web_server_env['PYTHONPATH'] = ':'.join(sys.path)
        web_server_process = subprocess.Popen([sys.executable, abspath('yadc_remote/manage.py'),
            'runserver', '0.0.0.0:%s' % str(web_server_port)], env=web_server_env)
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
