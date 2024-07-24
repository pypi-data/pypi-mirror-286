"""Mock objects for testing."""

import io
import json as pyjson
from wsgiref.headers import Headers
from wsgiref.util import setup_testing_defaults
from urllib.parse import urlencode, urlparse

HEADERS = {
    "HOST": "HTTP_HOST",
    "USER_AGENT": "HTTP_USER_AGENT",
}


def cookie2environ(cookies):
    """Convert to cookie (dict) to environ (dict).

    Returns:
        dict: {'HTTP_COOKIE': 'name1=val1; name2=val2...'}
    """
    l = [f'{cookie["name"]}={cookie["value"]}' for cookie in cookies.values()]
    if l:
        return {"HTTP_COOKIE": "; ".join(l)}
    else:
        return {}


def header2cookie(header):
    """Convert header (str) to cookie (dict)"""
    cookies = {}
    for s in header.get_all("Set-Cookie"):
        morsels = s.split("; ")
        name, value = morsels.pop(0).split("=")
        d = dict(name=name, value=value)
        for morsel in morsels:
            if morsel == "HttpOnly":
                d["httponly"] = True
            elif morsel == "Secure":
                d["secure"] = True
            else:
                key, val = morsel.split("=")
                key = key.lower().replace("-", "_")
                if key == "max_age":
                    d[key] = int(val)
                else:
                    d[key] = val
        cookies[name] = d
    return cookies


class Client:
    """Mock web browser, sends requests to app and receives responses.

    For simplicity it talks directly to the WSGI app instead of through a
    web server like gunicorn.
    """

    def __init__(self, prefix, app):
        self.prefix = prefix
        self.app = app
        self.cookies = {}
        self.headers = {"Host": prefix, "User-Agent": "MockClient"}
        Response.history = []

    def xform(self, name):
        """Convert header name to uppercase."""
        s = name.upper().replace("-", "_")
        return HEADERS.get(s, s)

    def get_environ(self, url, method, json, data):
        """Return environ dict for this URL."""
        parsed = urlparse(url)
        environ = {
            "PATH_INFO": parsed.path,
            "REQUEST_METHOD": method,
            "wsgi.url_scheme": parsed.scheme,
            "SERVER_NAME": parsed.netloc,
            "QUERY_STRING": parsed.query,
        }
        setup_testing_defaults(environ)
        headers = {self.xform(key): val for key, val in self.headers.items()}
        environ.update(headers)
        if data:
            encoded = urlencode(data)
            bstream = io.BytesIO(bytes(encoded, "utf-8"))
            environ["CONTENT_TYPE"] = "application/x-www-form-urlencoded"
            environ["CONTENT_LENGTH"] = bstream.getbuffer().nbytes
            environ["wsgi.input"] = bstream
        elif json:
            bstream = io.BytesIO(bytes(pyjson.dumps(json), "utf-8"))
            environ["CONTENT_TYPE"] = "application/json"
            environ["CONTENT_LENGTH"] = bstream.getbuffer().nbytes
            environ["wsgi.input"] = bstream
        environ.update(cookie2environ(self.cookies))
        return environ

    def delete(self, url, **kwargs):
        return self.handle_request("DELETE", url, **kwargs)

    def get(self, url, **kwargs):
        return self.handle_request("GET", url, **kwargs)

    def patch(self, url, **kwargs):
        return self.handle_request("PATCH", url, **kwargs)

    def post(self, url, **kwargs):
        return self.handle_request("POST", url, **kwargs)

    def put(self, url, **kwargs):
        return self.handle_request("PUT", url, **kwargs)

    def handle_request(
        self, method, url, allow_redirects=True, headers={}, json={}, data={}
    ):
        """Handle request.

        Args:
            method (str): 'DELETE', 'GET', 'PATCH', 'POST', 'PUT'.
            url (str): URL.
            allow_redirects: (bool). Default: True.
            headers (dict): client headers. Default: {}
            json (dict): JSON data. Default: {}
            data (dict): form data. Default: {}

        Returns:
            mock.Response object.
        """
        self.headers.update(headers)
        while True:
            environ = self.get_environ(url, method, json, data)
            response = Response(url=url)
            content = self.app(environ, response.start_response)
            response.load(content)
            self.cookies.update(response.cookies)
            if 300 <= response.status_code < 400 and allow_redirects:
                url = response.headers["Location"]
                Response.history.append(response)
            else:
                return response


class Response:
    """Wrapper of all info returned by server."""

    history = []

    def __init__(self, url):
        self.json = ""
        self.text = ""
        self.url = url

    def load(self, content):
        # WSGI callable returns iterable of bytes: convert to str.
        scontent = "".join(map(bytes.decode, content))
        if self.headers.get("Content-Type") == "application/json":
            self.json = pyjson.loads(scontent)
        else:
            self.text = scontent
            self.content = scontent

    def start_response(self, status, response_headers, exc_info=None):
        """Callback function to send HTTP status and headers to server."""
        self.headers = Headers(response_headers)
        self.cookies = header2cookie(self.headers)
        self.status = status
        self.status_code = int(self.status[:3])
