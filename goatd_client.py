from __future__ import print_function

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

import json

class Goat(object):
    def __init__(self, host='localhost', port=2222):
        self.host = host
        self.port = port

    def _url(self, endpoint):
        return 'http://{}:{}{}'.format(self.host, self.port, endpoint)

    def _get(self, endpoint):
        json_body = urlopen(self._url(endpoint)).read()
        return json.loads(json_body)

if __name__ == '__main__':
    goat = Goat()
    print(goat._get(''))
