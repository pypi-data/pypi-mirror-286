from io import BytesIO
import json
import unittest
from urllib.parse import urlencode

import drakken.exceptions
from drakken.message import Request, Response
from drakken.security import create_session_cookie


class TestRequest(unittest.TestCase):
    def test_cookie(self):
        env = {"REQUEST_METHOD": "GET", "HTTP_COOKIE": "fig=newton"}
        request = Request(env)
        self.assertEqual(request.cookies.get("fig"), "newton")

    def test_cookies(self):
        env = {
            "REQUEST_METHOD": "GET",
            "HTTP_COOKIE": "fig=newton; sugar=wafer",
        }
        request = Request(env)
        self.assertEqual(request.cookies.get("fig"), "newton")
        self.assertEqual(request.cookies.get("sugar"), "wafer")

    def test_invalid_cookie(self):
        # Seen in production.
        env = {"REQUEST_METHOD": "GET", "HTTP_COOKIE": "newton"}
        with self.assertRaises(drakken.exceptions.BadRequest):
            request = Request(env)

    def test_post_form(self):
        data = dict(email="kodos@earth.com", password="GreenMachine")
        # Convert dict into string.
        s = urlencode(data)
        # Convert str to bytes.
        bytes = str.encode(s)
        # Convert bytes into stream.
        stream = BytesIO(bytes)
        env = {
            "CONTENT_TYPE": "application/x-www-form-urlencoded",
            "CONTENT_LENGTH": len(bytes),
            "REQUEST_METHOD": "POST",
            "wsgi.input": stream,
            "HTTP_CONTENT_LENGTH": len(bytes),
            "HTTP_CONTENT_TYPE": "application/x-www-form-urlencoded",
        }
        request = Request(env)
        self.assertEqual(request.POST["email"], "kodos@earth.com")
        self.assertEqual(request.POST["password"], "GreenMachine")

    def test_post_json(self):
        data = dict(email="kodos@earth.com", password="GreenMachine")
        # Convert dict into string.
        s = json.dumps(data)
        # Convert str to bytes.
        bytes = str.encode(s)
        # Convert bytes into stream.
        stream = BytesIO(bytes)
        env = {
            "CONTENT_TYPE": "application/json",
            "CONTENT_LENGTH": len(bytes),
            "REQUEST_METHOD": "POST",
            "wsgi.input": stream,
        }
        request = Request(env)
        self.assertEqual(request.POST["email"], "kodos@earth.com")
        self.assertEqual(request.POST["password"], "GreenMachine")

    def test_query_string(self):
        env = {"REQUEST_METHOD": "GET", "QUERY_STRING": "color=yellow"}
        request = Request(env)
        self.assertEqual(request.GET["color"], "yellow")

    def test_url(self):
        env = {"REQUEST_METHOD": "GET", "HTTP_HOST": "http://testserver"}
        request = Request(env)
        self.assertEqual(request.url, "http://testserver")

    def test_url_path(self):
        env = {
            "REQUEST_METHOD": "GET",
            "HTTP_HOST": "http://testserver",
            "PATH_INFO": "/hello",
        }
        request = Request(env)
        self.assertEqual(request.url, "http://testserver/hello")

    def test_url_query_string(self):
        env = {
            "REQUEST_METHOD": "GET",
            "HTTP_HOST": "http://testserver",
            "PATH_INFO": "/hello",
            "QUERY_STRING": "color=yellow&year=1987",
        }
        request = Request(env)
        url = "http://testserver/hello?color=yellow&year=1987"
        self.assertEqual(request.url, url)


class TestResponse(unittest.TestCase):
    def test_status(self):
        response = Response()
        response.status_code = 404
        self.assertEqual(response.status, "404 Not Found")
        response.status_code = 500
        self.assertEqual(response.status, "500 Internal Server Error")

    def test_json(self):
        response = Response()
        self.assertEqual(response.content_type, "text/html")
        data = dict(email="kodos@earth.com", password="GreenMachine")
        response.json = data
        self.assertEqual(response.body, json.dumps(data).encode("utf-8"))
        self.assertEqual(response.content_type, "application/json")

    def test_default_headers(self):
        response = Response()
        self.assertEqual(response.headers, [("Content-Type", "text/html")])

    def test_cookie(self):
        sessionid = "howdy"
        cookie = create_session_cookie(sessionid)
        response = Response()
        response.set_cookie(**cookie)
        self.assertEqual(response.cookies, {"sessionid": cookie})
        header_name, header_value = response._set_cookie_headers()[0]
        s = "sessionid=howdy; Path=/; SameSite=strict; Max-Age=86400; HttpOnly"
        self.assertEqual(header_name, "Set-Cookie")
        self.assertEqual(header_value, s)

        # Do it again: cookie reader is destructive.
        header_name, header_value = response._set_cookie_headers()[0]
        self.assertEqual(header_name, "Set-Cookie")
        self.assertEqual(header_value, s)

    def test_multiple_cookies(self):
        c1 = dict(name="fig", value="newton")
        c2 = dict(name="sugar", value="wafer")
        response = Response()
        response.set_cookie(**c1)
        response.set_cookie(**c2)

        self.assertEqual(response.cookies["fig"], c1)
        self.assertEqual(response.cookies["sugar"], c2)
        headers = response._set_cookie_headers()
        self.assertEqual(headers[0][0], "Set-Cookie")
        self.assertEqual(headers[0][1], "fig=newton")
        self.assertEqual(headers[1][0], "Set-Cookie")
        self.assertEqual(headers[1][1], "sugar=wafer")


if __name__ == "__main__":
    unittest.main()
