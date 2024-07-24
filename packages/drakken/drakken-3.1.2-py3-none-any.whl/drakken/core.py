"""Routing module."""

import inspect
import logging
import mimetypes
import os
import re
import traceback

from parse import parse

from . import config
from . import exceptions
from .message import Response
from .mail import send_admins
from .middleware import Middleware
from .template import render

TEXT_FILE_TYPES = [
    "text/css",
    "text/csv",
    "text/html",
    "text/calendar",
    "application/javascript",
    "text/javascript",
    "text/plain",
    "text/xml",
]

logger = logging.getLogger(__name__)


class Drakken:
    """The Drakken Application class."""

    def __init__(self):
        """Initialize Drakken application."""
        self.routes = {}
        self.named_routes = {}
        # Middleware wraps around self (the application).
        self.middleware = Middleware(self)

    def __call__(self, environ, start_response):
        """WSGI API.

        Args:
            environ (dict): environment variables.
            start_response (function): callback function sending HTTP status
            and headers to server.

        Returns:
            list of bytes.
        """
        return self.middleware(environ, start_response)

    def _get_url_names(self, s):
        """Return list of URL names from string s.

        Args:
            s (str): string.

        Example:
            {% url login %}

        Returns:
            list: URL names found in s.
        """
        regex = r"\{\%\s*url\s+(.*?)\s*\%\}"
        return re.findall(regex, s)

    def _replace_url_name(self, name, path, s):
        """Replace url name with path in string s.

        Args:
            name (str): URL name.
            path (str): URL path.
            s (str): string.

        Example:
            {% url login %} becomes /account/login/

        Returns:
            String with named route variable replaced with route URL.
        """
        regex = r"\{\%\s*url\s+" + name + r"\s*\%\}"
        return re.sub(regex, path, s)

    def _load_named_routes(self, s):
        """Replace named route variables with the URL.

        Args:
            s (str): string.

        Example:
            {% url login %} becomes /account/login/

        Returns:
            str: named route variable replaced with route URL.
        """
        for name in self._get_url_names(s):
            try:
                path = self.named_routes[name]
                s = self._replace_url_name(name, path, s)
            except KeyError:
                pass
        return s

    def add_middleware(self, middleware):
        """Add middleware.

        Args:
            middleware (Middleware): Middleware object.
        """
        self.middleware.add(middleware)

    def _serve_static_file(self, request, response):
        """Serve static file."""
        paths = config.get("STATIC_PATHS")
        if config.get("STATIC_DIR"):
            paths.append(config.get("STATIC_DIR"))
        if not any([path for path in paths if request.path.startswith(path)]):
            # No static requests outside static dir or static paths.
            raise exceptions.Forbidden
        # Absolute path: use as is.
        elif os.path.exists(request.path):
            fpath = request.path
        # Relative path: convert to absolute path.
        else:
            fpath = os.path.abspath(request.path[1:])
        try:
            ftype = mimetypes.guess_type(fpath)[0]
            response.content_type = ftype
            if ftype in TEXT_FILE_TYPES:
                with open(fpath, "r", encoding="ISO-8859-1") as f:
                    response.text = f.read()
            else:
                with open(fpath, "rb") as f:
                    response.body = f.read()
            return response
        except (FileNotFoundError, IsADirectoryError):
            raise exceptions.NotFound

    def _not_found(self, response):
        """Return 404 response."""
        response.status_code = 404
        template_path = os.path.join(config.get("TEMPLATE_DIR"), "404.html")
        if os.path.exists(template_path):
            response.text = render(response, "404.html")
        else:
            response.text = "Not found."

    def _find_handler(self, path):
        """Find the request handler for this request path.

        Args:
            path (str): URL path.

        Returns:
            page controller, URL parameter.
        """
        for request_path, handler in self.routes.items():
            parsed = parse(request_path, path)
            if parsed:
                return handler, parsed.named
        return None, None

    def handle_request(self, request):
        """Find and execute the handler for this request.

        Args:
            request (message.Request): Request object.

        Returns:
            message.Response object.
        """
        response = Response()
        try:
            handler, kwargs = self._find_handler(path=request.path)
            if handler:
                # If request.method (POST, GET, PUT, PATCH, DELETE) isn't
                # implemented in the request handler, return 400.
                if inspect.isclass(handler):
                    handler = getattr(handler(), request.method.lower(), None)
                    if not handler:
                        raise exceptions.BadRequest
                handler(request, response, **kwargs)
                if response.text:
                    response.text = self._load_named_routes(response.text)
            elif mimetypes.guess_type(request.path)[0]:
                self._serve_static_file(request, response)
            else:
                self._check_trailing_slash(request)
                # Default handler: 404 not found.
                raise exceptions.NotFound
        except exceptions.BadRequest:
            response.status_code = 400
            response.text = "Bad Request"
        except exceptions.Forbidden:
            response.status_code = 403
            response.text = "Forbidden"
        except exceptions.HTTPRedirect as exc:
            response.status_code = exc.status_code
            response.location = exc.path
        except exceptions.LoginFail:
            response.status_code = 401
            response.text = "Unauthorized"
        except exceptions.NotFound:
            self._not_found(response)
        except Exception:
            # Universal catch-all for server errors.
            if config.get("DEBUG"):
                raise
            subject = f'{config.get("APP_NAME")} server error'
            body = traceback.format_exc()
            send_admins(subject, body)
            logger.error(f"500 ERROR {body}")
            response.status_code = 500
            response.text = "Internal Server Error"
        return response

    def register_blueprint(self, blueprint):
        """Store blueprint.

        Args:
            blueprint (Blueprint): a Blueprint object.
        """
        for route, handler in blueprint.routes.items():
            path = f"{blueprint.url_prefix}{route}".replace("//", "/")
            self.routes[path] = handler
            # Store the name for this route
            for key in blueprint.named_routes:
                if blueprint.named_routes[key] == route:
                    self.named_routes[key] = path
                    continue

    def route(self, path, name=""):
        """Decorator to store route.

        Args:
            path (str): URL path.
            name (str): route name, optional.

        Raises:
            AssertionError: Route already exists.
        """
        if path in self.routes:
            raise AssertionError("Route already exists.")

        def wrapper(handler):
            self.named_routes[name] = path
            self.routes[path] = handler
            return handler

        return wrapper

    def runserver(self):
        """Run development server forever."""
        from wsgiref.simple_server import make_server

        with make_server("", 8000, self) as httpd:
            print("Starting development server at http://127.0.0.1:8000")
            print("Quit the server with CONTROL-C.")
            httpd.serve_forever()

    def _check_trailing_slash(self, request):
        """Search for URI with and without a trailing slash.

        Maybe the user forgot a trailing slash or added one by mistake.

        Args:
            request (Request): Request object.

        Raises:
            exceptions.HTTPRedirect: alternative route found.
        """
        if not config.get("TRAILING_SLASH_REDIRECT"):
            return
        if request.path.endswith("/"):
            path = request.path[:-1]
        else:
            path = request.path + "/"
        handler, kwargs = self._find_handler(path=path)
        if handler:
            raise exceptions.HTTPRedirect(path=path, status_code=301)


class Blueprint:
    """A container for storing related page handlers.

    Allows you to divide an app into logical components: an accounts
    blueprint, a documents blueprint, etc.

    Args:
        name (str): blueprint name.
        url_prefix (str): URL prefix.
    """

    def __init__(self, name, url_prefix=""):
        self.name = name
        self.url_prefix = url_prefix
        self.routes = {}
        self.named_routes = {}

    def route(self, path, name=""):
        """Decorator to store route.

        Args:
            path (str): URL path.
            name (str): route name, optional.

        Raises:
            AssertionError: Route already exists in the blueprint.
        """
        if path in self.routes:
            raise AssertionError("Route already exists.")

        def wrapper(handler):
            self.named_routes[name] = path
            self.routes[path] = handler
            return handler

        return wrapper
