from httpretty import HTTPretty, httprettified

from goatd_client import Goat

@httprettified
class TestGoatdClient(object):
    def setup(self):
        self.goat = Goat()

    def test_root(self):
        HTTPretty.register_uri(HTTPretty.GET, 'http://localhost:2222/',
                               body='{"goatd": {"version": "0.1mock"}}')
        assert self.goat.version

    def test_heading(self):
        HTTPretty.register_uri(HTTPretty.GET, 'http://localhost:2222/heading',
                               body='{"result": 2.43}')
        assert self.goat.heading == 2.43

    def test_wind(self):
        HTTPretty.register_uri(HTTPretty.GET, 'http://localhost:2222/wind',
                               body='{"direction": 8.42}')
        assert self.goat.wind.direction == 8.42
