import tservers

"""
    A collection of errors turned up by fuzzing. Errors are integrated here
    after being fixed to check for regressions.
"""

class TestFuzzy(tservers.HTTPProxTest):
    def test_idna_err(self):
        req = r'get:"http://localhost:%s":i10,"\xc6"'
        p = self.pathoc()
        assert p.request(req%self.server.port).status_code == 400

    def test_nullbytes(self):
        req = r'get:"http://localhost:%s":i19,"\x00"'
        p = self.pathoc()
        assert p.request(req%self.server.port).status_code == 400

    def test_invalid_ports(self):
        req = 'get:"http://localhost:999999"'
        p = self.pathoc()
        assert p.request(req).status_code == 400

    def test_invalid_ipv6_url(self):
        req = 'get:"http://localhost:%s":i13,"["'
        p = self.pathoc()
        assert p.request(req%self.server.port).status_code == 400

    def test_invalid_upstream(self):
        req = r"get:'http://localhost:%s/p/200:i10,\'+\''"
        p = self.pathoc()
        assert p.request(req%self.server.port).status_code == 502

    def test_upstream_disconnect(self):
        req = r'200:d0:h"Date"="Sun, 03 Mar 2013 04:00:00 GMT"'
        p = self.pathod(req)
        assert p.status_code == 400


