"""Middleware module.

Middleware acts as a middleman between the web server and your app. The
middleware wraps around the app, allowing it to modify a request before your
app receives it or modify a response after your app processes it. An app can
have several middleware, all wrapped around the app like the layers of an onion.
"""

from .message import Request, Response
from .exceptions import BadRequest, CSRFTokenFail, Forbidden
from .model import validate_CSRF


class Middleware:
    """Parent class.

    To create a middleware, subclass this class and override
    `process_request` or `process_response`.

    Args:
        app: The drakken.core.Drakken object this middleware handles.
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        """WSGI API.

        Args:
            environ (dict): environment variables.
            start_response (function): callback function sending HTTP status
            and headers to server.

        Returns:
            list of bytes.
        """
        try:
            request = Request(environ)
            response = self.app.handle_request(request)
        except BadRequest:
            response = Response(status_code=400, text="Bad Request")
        finally:
            return response(environ, start_response)

    def add(self, middleware):
        """Wrap another middleware around the app.

        Allows you to daisy-chain multiple middleware to an app.

        Args:
            middleware (Middleware): Middleware object.
        """
        self.app = middleware(self.app)

    def handle_request(self, request):
        """Execute the handler for this request.

        Args:
            request (Request): Request object.
        """
        try:
            self.process_request(request)
            response = self.app.handle_request(request)
        except BadRequest:
            return Response(status_code=400, text="Bad Request")
        except Forbidden:
            return Response(status_code=403, text="Forbidden")
        self.process_response(request, response)
        return response

    def process_request(self, request):
        """Child class overrides this method."""
        pass

    def process_response(self, request, response):
        """Child class overrides this method."""
        pass


class CSRFMiddleware(Middleware):
    """Validate CSRF token if request attempts to modify the system."""

    def process_request(self, request):
        """Validate CSRF token if request alters system state.

        Args:
            request (Request): Request object.

        Raises:
            Forbidden: Invalid CSRF token.
        """
        if request.method != "GET":
            try:
                validate_CSRF(request)
            except CSRFTokenFail:
                raise Forbidden
