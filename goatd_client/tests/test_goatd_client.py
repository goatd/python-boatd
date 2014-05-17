from httpretty import HTTPretty, httprettified

from goatd_client import Goat

@httprettified
class TestGoatdClient(object):
    def setup(self):
        self.goat = Goat()

    def test_root(self):
        HTTPretty.register_uri(HTTPretty.GET, 'http://localhost:2222/',
                               body='{"goatd": {"version": "0.1mock"}}')
        print self.goat.version()
