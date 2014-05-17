from __future__ import print_function

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

import json

class Goat(object):
    def __init__(self, host='localhost', port=2222):
        self.host = host
        self.port = port

    def _url(self, endpoint):
        return 'http://{0}:{1}{2}'.format(self.host, self.port, endpoint)

    def _get(self, endpoint):
        json_body = urlopen(self._url(endpoint)).read().decode('utf-8')
        return json.loads(json_body)

    def _post(self, content, endpoint=''):
        url = self._url(endpoint)
        post_content = json.dumps(content).encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        request = Request(url, post_content, headers)
        return urlopen(request)

    def heading(self):
        content = self._get('/heading')
        return content.get('result')

    def wind(self):
        content = self._get('/wind')
        return content.get('result')

    def position(self):
        content = self._get('/position')
        return tuple(content.get('result'))

    def version(self):
        content = self._get('/')
        return content.get('goatd').get('version')

    def rudder(self, angle):
        request = self._post({'value': angle}, '/rudder')
        content = json.loads(request.read().decode('utf-8'))
        return content.get('result')

    def sail(self, angle):
        request = self._post({'value': angle}, '/sail')
        content = json.loads(request.read().decode('utf-8'))
        return content.get('result')

if __name__ == '__main__':
    goat = Goat()
    print(goat._get(''))
    print(goat.version())
    print(goat.heading())
    print(goat.wind())
    print(goat.position())
    print(goat.rudder(0))
    print(goat.rudder(10))

