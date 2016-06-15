from __future__ import print_function

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

from collections import namedtuple
import json

from .bearing import Bearing
from .point import Point


Wind = namedtuple('Wind', ['direction', 'speed', 'relative_direction'])


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

    @property
    def version(self):
        '''Return the version of goatd'''
        content = self.goatd.get('/')
        return content.get('goatd').get('version')


class Goat(object):
    '''A goat controlled by goatd'''

    def __init__(self, goatd=None):
        if goatd is None:
            self.goatd = Goatd()
        else:
            self.goatd = goatd

    @property
    def heading(self):
        '''
        Return the current heading of the goat in degrees.

        :returns: current bearing
        :rtype: Bearing
        '''
        content = self.goatd.get('/goat')
        return Bearing(float(content.get('heading')))

    @property
    def wind(self):
        '''
        Return the direction of the wind in degrees.

        :returns: wind object containing direction bearing and speed
        :rtype: Wind
        '''
        content = self.goatd.get('/wind')
        return Wind(
            Bearing(content.get('direction')) - self.heading,
            content.get('speed'),
            Bearing(content.get('direction'))
        )

    @property
    def relative_wind(self):
        '''
        Return the direction of the wind, relative to the goat's current
        direction.

        :returns: wind direction bearing in goat coordinates
        :rtype: Bearing
        '''
        return self.wind.direction

    @property
    def position(self):
        '''
        Return the current position of the goat.

        :returns: current position
        :rtype: Point
        '''
        content = self.goatd.get('/goat')
        lat, lon = content.get('position')
        return Point(lat, lon)

    def set_rudder(self, angle):
        '''
        Set the angle of the rudder to be `angle` degrees.

        :param angle: rudder angle
        :type angle: float between -90 and 90
        '''
        angle = float(angle)
        request = self.goatd.post({'value': float(angle)}, '/rudder')
        return request.get('result')

    def set_sail(self, angle):
        '''
        Set the angle of the sail to `angle` degrees

        :param angle: sail angle
        :type angle: float between -90 and 90
        '''
        angle = float(angle)
        request = self.goatd.post({'value': float(angle)}, '/sail')
        return request.get('result')


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
        d = self.goatd.post({'active': name}, endpoint='/behaviours')
        current = d.get('active')
        if current is not None:
            return 'started {}'.format(current)
        else:
            return 'no behaviour running'

    def stop(self):
        '''
        Stop the current behaviour.
        '''
        self.start(None)


def get_current_waypoints(goatd=None):
    '''
    Get the current set of waypoints active from goatd.

    :returns: The current waypoints
    :rtype: List of Points
    '''

    if goatd is None:
        goatd = Goatd()

    content = goatd.get('/waypoints')
    return [Point(*coords) for coords in content.get('waypoints')]


def get_home_position(goatd=None):
    '''
    Get the current home position from goatd.

    :returns: The configured home position
    :rtype: Points
    '''

    if goatd is None:
        goatd = Goatd()

    content = goatd.get('/waypoints')
    home = content.get('home', None)
    if home is not None:
        lat, lon = home
        return Point(lat, lon)
    else:
        return None


if __name__ == '__main__':
    goat = Goat()
    print(goat.version)
    print(goat.heading)
    print(goat.wind)
    print(goat.position)
    print(goat.rudder(0))
    print(goat.rudder(10))
