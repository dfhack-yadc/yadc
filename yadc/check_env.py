# Check environment, install required packages, etc.

import importlib, os, random

import yadc.util

required_modules = ['django']

def check_env():
    for module in required_modules:
        try:
            globals().setdefault(module, importlib.import_module(module))
        except ImportError as e:
            print('Module not found: %s' % module)
            return False
    if not django.get_version().startswith('1.7.'):
        print('Django 1.7.x expected, %s found' % django.get_version())
        return False
    print('Django version %s' % django.get_version())
    secret_path = yadc.util.abspath('yadc_remote/secret.txt')
    if not os.path.exists(secret_path):
        print('Generating secret key')
        with open(secret_path, 'w') as f:
            f.write(''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
                for i in range(50)]))
    return True
