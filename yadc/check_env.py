# Check environment, install required packages, etc.

import importlib

required_modules = ['django']

def check_env():
    for module in required_modules:
        try:
            importlib.import_module(module)
        except ImportError as e:
            print('Module not found: %s' % module)
            return False
    return True
