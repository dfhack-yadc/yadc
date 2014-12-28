# Check environment, install required packages, etc.

import importlib, os, re, sys
import hashlib, tarfile, zipfile

import yadc.util

if yadc.util.py2:
    from urllib import urlretrieve
else:
    from urllib.request import urlretrieve

required_modules = {
    'django': {
        'url': 'https://pypi.python.org/packages/source/D/Django/Django-1.7.1.tar.gz',
        'md5': '81dae89f21647b9aa5c46c6b7dbfa349',
        'module_path': 'Django-1.7.1/django'
    }
}
for module in required_modules:
    info = required_modules[module]
    if 'url' not in info or 'md5' not in info or 'module_path' not in info:
        raise ValueError("Invalid module requirement: %s" % module)
    info['url'] = info['url'].replace('\\', '/')
    info['module_path'] = info['module_path'].replace('\\', '/').split('/')

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
    print('Django version %s: %s' % (django.get_version(),
        os.path.dirname(yadc.util.relpath(django.__file__))))
    if not os.path.exists(yadc.util.abspath('yadc_remote/secret.txt')):
        print('Generating secret key')
        yadc.util.new_secret_key()
    return True

def try_install(module):
    """ Install a package into depends/

    This assumes that packages are distributed in .tar.{gz,bz2} format
    """
    if module not in required_modules:
        raise ValueError('Unrecognized module')
    info = required_modules[module]
    archive_path = os.path.join('depends', info['url'].split('/')[-1])
    if os.path.exists(archive_path):
        print('Already downloaded: %s' % archive_path)
    else:
        print('Downloading %s' % info['url'])
        urlretrieve(info['url'], archive_path)
    with open(archive_path, 'rb') as f:
        md5 = hashlib.md5(f.read()).hexdigest()
        if md5 != info['md5']:
            raise ValueError('MD5 mismatch: Expected %s, actual %s' % (info['md5'], md5))
    print('Unpacking %s' % archive_path)
    archive = tarfile.open(archive_path)
    archive.extractall(path='depends')
    archive.close()
    os.rename(os.path.join('depends', *info['module_path']),
              os.path.join('depends', module))
    return True
