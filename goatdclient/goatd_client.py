from __future__ import print_function

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

from collections import namedtuple
import json

from .bearing import Bearing
from .point import Point


Wind = namedtuple('Wind', ['direction', 'speed'])


class Goatd(object):
    def __init__(self, host='localhost', port=2222):
        '''
        Create a goat instance, connecting to goatd at `host` on port `port`
        '''
        self.host = host
        self.port = port

    def url(self, endpoint):
        '''Return a formatted url pointing at `endpoint` on the goatd server'''
        return 'http://{0}:{1}{2}'.format(self.host, self.port, endpoint)

    def get(self, endpoint):
        '''Return the result of a GET request to `endpoint` on goatd'''
        json_body = urlopen(self.url(endpoint)).read().decode('utf-8')
        return json.loads(json_body)

    def post(self, content, endpoint=''):
        '''
        Issue a POST request with `content` as the body to `endpoint` and
        return the result.
        '''
        url = self.url(endpoint)
        post_content = json.dumps(content).encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        request = Request(url, post_content, headers)

        response = urlopen(request)

        return json.loads(response.read().decode('utf-8'))

    def quit(self):
        content = self.post({'quit': True}, '/')
        print(content)


class LegacyGoat(object):
    '''
    A goat controlled by goatd. This is the legacy goat interface for backwards
    compatibility. Deprecated.
    '''

    def __init__(self, goatd=None):
        if goatd is None:
            self.goatd = Goatd()
        else:
            self.goatd = goatd

    @property
    def heading(self):
        '''Return the current heading of the goat in degrees'''
        content = self.goatd.get('/goat')
        return float(content.get('heading'))

    @property
    def wind(self):
        '''Return the direction of the wind in degrees'''
        content = self.goatd.get('/wind')
        return Wind(content.get('direction'), content.get('speed'))

    @property
    def position(self):
        '''Return a tuple in the form `(latitude, longitude)`'''
        content = self.goatd.get('/goat')
        return tuple(content.get('position'))

    @property
    def version(self):
        '''Return the version of goatd'''
        content = self.goatd.get('/')
        return content.get('goatd').get('version')

    def rudder(self, angle):
        '''Set the angle of the rudder to be `angle` degrees'''
        request = self.goatd.post({'value': angle}, '/rudder')
        content = json.loads(request.read().decode('utf-8'))
        return content.get('result')

    def sail(self, angle):
        '''Set the angle of the sail to `angle` degrees'''
        request = self.goatd.post({'value': angle}, '/sail')
        content = json.loads(request.read().decode('utf-8'))
        return content.get('result')


class ConvenienceGoat(object):
    '''A goat controlled by goatd'''

    def __init__(self, goatd=None):
        if goatd is None:
            self.goatd = Goatd()
        else:
            self.goatd = goatd

    @property
    def heading(self):
        '''Return the current heading of the goat in degrees'''
        content = self.goatd.get('/goat')
        return Bearing(float(content.get('heading')))

    @property
    def wind(self):
        '''Return the direction of the wind in degrees'''
        content = self.goatd.get('/wind')
        return Wind(Bearing(content.get('direction')), content.get('speed'))

    @property
    def position(self):
        '''Return a tuple in the form `(latitude, longitude)`'''
        content = self.goatd.get('/goat')
        lat, lon = content.get('position')
        return Point(lat, lon)

    @property
    def version(self):
        '''Return the version of goatd'''
        content = self.goatd.get('/')
        return content.get('goatd').get('version')

    def rudder(self, angle):
        '''Set the angle of the rudder to be `angle` degrees'''
        request = self.goatd.post({'value': float(angle)}, '/rudder')
        content = json.loads(request.read().decode('utf-8'))
        return content.get('result')

    def sail(self, angle):
        '''Set the angle of the sail to `angle` degrees'''
        request = self.goatd.post({'value': float(angle)}, '/sail')
        content = json.loads(request.read().decode('utf-8'))
        return content.get('result')


def Goat(convenience=False, *args, **kwargs):
    '''
    Return a Goat instance. If ``convenience`` is True, return an instance of
    ``ConvenienceGoat``, otherwise return ``LegacyGoat``.
    '''
    if convenience is True:
        return ConvenienceGoat(*args, **kwargs)
    else:
        return LegacyGoat(*args, **kwargs)


class Behaviour(object):
    def __init__(self, goatd=None):
        if goatd is None:
            self.goatd = Goatd()
        else:
            self.goatd = goatd

    def _get_behaviour_data(self):
        return self.goatd.get('/behaviours')

    def list(self):
        '''Return a list of the available behaviours to run.'''
        return list(self._get_behaviour_data().get('behaviours').keys())

    def start(self, name):
        '''
        End the current behaviour and run a named behaviour.

        :param name: the name of the behaviour to run
        :type name: str
        '''
        d = self.goatd.post({'current': name}, endpoint='/behaviours')
        current = d.get('current')
        if current is not None:
            return 'started {}'.format(current)
        else:
            return 'no behaviour running'

    def stop(self):
        '''
        Stop the current behaviour.
        '''
        self.start(None)


if __name__ == '__main__':
    goat = Goat()
    print(goat.version)
    print(goat.heading)
    print(goat.wind)
    print(goat.position)
    print(goat.rudder(0))
    print(goat.rudder(10))
