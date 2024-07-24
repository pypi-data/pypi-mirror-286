from http import HTTPStatus
import json
from urllib.parse import parse_qs, parse_qsl, urljoin

from .exceptions import BadRequest


class Request:
    def __init__(self, environ):
        """Initialize request.

        Args:
            environ (dict): CGI environment variables.
        """
        self.client_addr = environ.get("REMOTE_ADDR")
        self.cookies = {}
        self.environ = environ
        self.GET = {}
        self.host = environ.get("HTTP_HOST")
        self.POST = {}
        self.method = environ.get("REQUEST_METHOD")
        self.path = environ.get("PATH_INFO")
        self.query_string = environ.get("QUERY_STRING")
        self.url = urljoin(self.host, self.path)
        if self.query_string and self.url:
            self.url += "?" + environ.get("QUERY_STRING")
        self.user_agent = environ.get("HTTP_USER_AGENT")
        if self.method == "GET":
            self.GET = dict(parse_qsl(self.environ.get("QUERY_STRING")))
        elif self.method == "POST":
            self._set_post()
        self._set_cookies()

    def _set_cookies(self):
        cookie_str = self.environ.get("HTTP_COOKIE")
        if cookie_str:
            cookies = cookie_str.split("; ")
            for cookie in cookies:
                try:
                    name, val = cookie.split("=")
                    self.cookies[name] = val
                except ValueError:
                    raise BadRequest

    def _set_post(self):
        stream = self.environ.get("wsgi.input")
        content_length = self.environ.get("CONTENT_LENGTH")
        # In case the request has no payload.
        if content_length:
            data = stream.read(int(content_length)).decode()
        content_type = self.environ.get("CONTENT_TYPE")
        if content_type == "application/x-www-form-urlencoded":
            self.POST = dict(parse_qsl(data))
        elif content_type == "application/json":
            self.POST = json.loads(data)


class Response:
    def __init__(self, status_code=200, text=""):
        """Initialize response.

        Args:
            status_code (int): HTTP response status code.
            text (str): text string.
        """
        self.cookies = {}
        self.location = None
        self.status_code = status_code
        self.text = text
        self._json = ""
        self.content_type = "text/html"
        self.body = ""

    @property
    def headers(self):
        """Return list of header tuples."""
        return self._set_headers()

    @property
    def json(self):
        """Return json."""
        return self._json

    @json.setter
    def json(self, value):
        """Set body to json string and set content-type: application/json.

        Arguments:
            value: object to be converted to json string.
        """
        self._json = value
        self.body = json.dumps(value).encode("utf-8")
        self.content_type = "application/json"

    @property
    def status(self):
        """Return HTTP status string."""
        return f"{self.status_code} {HTTPStatus(self.status_code).phrase}"

    def __call__(self, environ, start_response):
        """WSGI API.

        Args:
            environ (dict): environment variables.
            start_response (function): callback function sending HTTP status
            and headers to server.

        Returns:
            list of bytes.
        """
        response_headers = self._set_headers()
        start_response(self.status, response_headers)
        if self.body:
            return [self.body]
        else:
            return [self.text.encode("utf-8")]

    def _set_content_length_header(self):
        if self.body:
            length = str(len(self.body))
        else:
            length = str(len(self.text.encode("utf-8")))
        return "Content-Length", length

    def set_cookie(self, **kwargs):
        """Set cookie.

        Args:
            **kwargs: cookie dictionary. Required keys: 'name' and 'value'.
        """
        name = kwargs.get("name")
        self.cookies[name] = kwargs

    def _cookie2header(self, cookie):
        """Convert cookie (dict) into header (str)."""
        s = f'{cookie["name"]}={cookie["value"]}'
        path = cookie.get("path")
        if path:
            s += f"; Path={path}"
        samesite = cookie.get("samesite")
        if samesite:
            s += f"; SameSite={samesite}"
        max_age = cookie.get("max_age")
        if max_age:
            s += f"; Max-Age={max_age}"
        # Secure and HttpOnly don't have values.
        if cookie.get("httponly"):
            s += "; HttpOnly"
        if cookie.get("secure"):
            s += "; Secure"
        return s

    def _set_cookie_headers(self):
        """Return list of cookie header tuples."""
        return [
            ("Set-Cookie", self._cookie2header(item)) for item in self.cookies.values()
        ]

    def _set_content_type_header(self):
        return "Content-Type", self.content_type

    def _set_headers(self):
        """Create list of header tuples.

        Note:
            PEP 3333--HTTP Date and Server headers are normally supplied by
            the server or gateway.
        """
        headers = self._set_cookie_headers()
        if 300 <= self.status_code < 400:
            # Redirect has no content.
            headers.append(self._set_location_header())
        else:
            headers.append(self._set_content_type_header())
            content_length_header = self._set_content_length_header()
            if content_length_header[1] != "0":
                headers.append(content_length_header)
        return headers

    def _set_location_header(self):
        return "Location", self.location
