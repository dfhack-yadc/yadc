# Check environment, install required packages, etc.

import importlib, os, re, sys
import tarfile, zipfile

import yadc.util

required_modules = ['django']

def check_env():
    for module in required_modules:
        try:
            globals().setdefault(module, importlib.import_module(module))
        except ImportError:
            print('Module not found: %s' % module)
            try:
                if not try_install(module):
                    raise Exception
                globals().setdefault(module, importlib.import_module(module))
            except Exception as e:
                print('Failed to install %s: %s' % (module, e if e else '(unknown)'))
                return False
    if not django.get_version().startswith('1.7.'):
        print('Django 1.7.x expected, %s found' % django.get_version())
        return False
    print('Django version %s' % django.get_version())
    if not os.path.exists(yadc.util.abspath('yadc_remote/secret.txt')):
        print('Generating secret key')
        yadc.util.new_secret_key()
    return True

def try_install(module):
    """ Install a package from PyPI into depends/

    This assumes that pip is insalled and packages are distributed in
    .tar.{gz,bz2} format and unpack into the following structure:
    Package-x.x.x/
        (distutils-related files)
        package/
            __init__.py
            (package code)
    """
    pattern = re.compile(r'%s.+?(tar\.gz|tar\.bz2)' % module, re.IGNORECASE)
    matches = filter(pattern.match, os.listdir('depends'))
    if not len(matches):
        try:
            import pip
        except ImportError:
            print('pip not found - cannot install dependencies')
            return False
        try:
            pip.main(['install', '--download', 'depends', module])
        except (Exception, SystemExit) as e:
            print(e if e else "An unknown error occured")
            return False
    else:
        print('Already downloaded.')
    matches = filter(pattern.match, os.listdir('depends'))
    match = matches[0]
    if not len(matches):
        raise Exception('Archive for %s not found' % module)
    archive_path = os.path.join('depends', match)
    print('Unpacking %s (%s)' % (module, archive_path))
    archive = tarfile.open(archive_path)
    archive.extractall(path='depends')
    archive.close()
    os.rename(os.path.join('depends', match.split('.tar')[0], module),
              os.path.join('depends', module))
    return True
