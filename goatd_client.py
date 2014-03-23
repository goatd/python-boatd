try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

class Goat(object):
    def __init__(self):
        self.port = 2222
        self.host = 'http://localhost:{}{}'

    def _get(self, endpoint):
        return json.loads(urlopen(self.host.format(self.port, endpoint)))
