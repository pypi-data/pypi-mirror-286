"""Test harness for mock client."""

import logging
import unittest
from wsgiref.headers import Headers

from drakken.core import Drakken
from drakken.mock import Client, cookie2environ, header2cookie


class TestClient(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.WARNING)
        self.app = Drakken()
        self.client = Client(prefix="http://testserver", app=self.app)

    def test_cookie2environ(self):
        c1 = dict(name="fig", value="newton")
        c2 = dict(name="foo", value="bar")
        d = {"fig": c1, "foo": c2}
        environ = cookie2environ(d)
        self.assertEqual(environ, {"HTTP_COOKIE": "fig=newton; foo=bar"})

    def test_cookie_persist(self):
        # Client should use cookie in all requests.
        c1 = dict(name="fig", value="newton")
        c2 = dict(name="dog", value="beagle")

        @self.app.route("/foo")
        def foo(request, response):
            # Attach cookies to response.
            response.cookies["fig"] = c1
            response.cookies["dog"] = c2
            response.text = "foo"

        @self.app.route("/bar")
        def bar(request, response):
            # Read cookies from request and return as json.
            response.json = request.cookies

        url = "http://testserver/foo"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.cookies.get("fig"), c1)
        self.assertEqual(response.cookies.get("fig"), c1)
        self.assertEqual(self.client.cookies.get("dog"), c2)
        self.assertEqual(response.cookies.get("dog"), c2)

        url = "http://testserver/bar"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.cookies.get("fig"), c1)
        self.assertEqual(response.json, {"fig": "newton", "dog": "beagle"})

    def test_custom_headers(self):
        s = "Calm, steamy morning."
        headers = {"User-Agent": "boop"}

        @self.app.route("/home")
        def home(request, response):
            response.text = s

        url = "http://testserver/home"
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, s)
        self.assertEqual(self.client.headers["User-Agent"], "boop")

    def tearDown(self):
        logging.disable(logging.NOTSET)


class TestHeader2Cookie(unittest.TestCase):
    def test_simple_cookie(self):
        h = [
            ("Set-Cookie", "fig=newton"),
            ("Content-Type", "text/html"),
            ("Content-Length", "3"),
        ]
        headers = Headers(h)
        c = dict(name="fig", value="newton")
        d = {"fig": c}
        self.assertEqual(header2cookie(headers), d)

    def test_multiple_cookies(self):
        h = [
            ("Set-Cookie", "fig=newton"),
            ("Set-Cookie", "foo=bar"),
            ("Content-Type", "text/html"),
            ("Content-Length", "3"),
        ]
        headers = Headers(h)
        c1 = dict(name="fig", value="newton")
        c2 = dict(name="foo", value="bar")
        d = {"fig": c1, "foo": c2}
        self.assertEqual(header2cookie(headers), d)

    def test_session_cookie(self):
        s = "sessionid=blah; path=/; HttpOnly; Secure; SameSite=strict; Max-Age=1800"
        h = [
            ("Set-Cookie", s),
            ("Content-Type", "text/html"),
            ("Content-Length", "3"),
        ]
        headers = Headers(h)
        cookie = dict(
            name="sessionid",
            value="blah",
            path="/",
            secure=True,
            httponly=True,
            samesite="strict",
            max_age=1800,
        )
        self.assertEqual(header2cookie(headers), {"sessionid": cookie})


if __name__ == "__main__":
    unittest.main()
