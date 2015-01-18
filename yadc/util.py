import os, random, sys, threading, time

py_version = int(sys.version[0])
py2 = (py_version == 2)
py3 = (py_version == 3)

def printl(*args):
    sys.stdout.write(*args)
    sys.stdout.flush()

# Prevent interleaved output from separate threads
# Note that this does not affect external code and/or code that uses print(),
# notably the web server
_log_lock = threading.Lock()
def log(msg, prepend='[yadc]', type=None, newline=True):
    with _log_lock:
        printl(time.strftime('[%d/%b/%Y %H:%M:%S] ') +
            ((prepend + ' ') if prepend else '') +
            (('[%s] ' % type) if type else '') +
            msg + ('\n' if newline else ''))

def log_wrapper(type):
    def wrapper(*args, **kwargs):
        return log(type=type, *args, **kwargs)
    return wrapper

warn = log_wrapper('warning')
err = log_wrapper('error')

def rootpath():
    return os.path.dirname(os.path.dirname(__file__))

def abspath(path):
    return os.path.join(rootpath(), *path.replace('\\', '/').split('/'))

def relpath(path):
    return path.replace(rootpath(), '.')

def update_path():
    """ Add depends/ directory to sys.path """
    depends_dir = abspath('depends')
    if not os.path.isdir(depends_dir):
        os.mkdir(depends_dir)
    if depends_dir not in sys.path:
        sys.path.insert(sys.path.index('') if '' in sys.path else 0, depends_dir)

def get_secret_key():
    path = abspath('yadc_remote/secret.txt')
    try:
        return open(path).read().strip()
    except IOError:
        raise IOError("Failed to retrieve secret key from %s" % path)

def new_secret_key(overwrite=False):
    secret_path = abspath('yadc_remote/secret.txt')
    if overwrite or not os.path.exists(secret_path):
        with open(secret_path, 'w') as f:
            f.write(''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
                for i in range(50)]))
            f.write('\n')
