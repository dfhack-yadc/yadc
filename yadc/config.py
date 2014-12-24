import json

class Config:
    def __init__(self, path=''):
        self.data = {}
        if path:
            self.load(path)
    def load(self, path):
        with open(path) as f:
            self.data = json.load(f)
        self.path = path
    def save(self, path=''):
        if not path:
            path = self.path
        with open(path, 'w') as f:
            json.dump(self.data, f)
    def __getattr__(self, attr):
        if hasattr(self.data, attr):
            return getattr(self.data, attr)
        raise AttributeError
