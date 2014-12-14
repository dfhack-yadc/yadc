import os

def rootpath():
    return os.path.dirname(os.path.dirname(__file__))

def abspath(path):
    return os.path.join(rootpath(), *path.split('/'))

def get_secret_key():
    path = abspath('yadc_remote/secret.txt')
    try:
        return open(path).read().strip()
    except IOError:
        raise IOError("Failed to retrieve secret key from %s" % path)
