import logging
import os
import tempfile
import unittest

from drakken.config import loads
from drakken.core import Drakken, Blueprint
from drakken.exceptions import redirect
from drakken.mock import Client
from drakken.template import render


class TestCore(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.WARNING)
        self.app = Drakken()
        self.client = Client(prefix="http://testserver", app=self.app)

    def test_basic_route(self):
        s = "Calm, steamy morning."

        @self.app.route("/home")
        def home(request, response):
            response.text = s

        url = "http://testserver/home"
        self.assertEqual(self.client.get(url).text, s)

    def test_blueprint(self):
        s = "Calm, steamy morning."
        bp = Blueprint(name="account", url_prefix="/customer-account")

        @bp.route("/home")
        def home(request, response):
            response.text = s

        self.app.register_blueprint(bp)
        url = "http://testserver/customer-account/home"
        self.assertEqual(self.client.get(url).text, s)

    def test_redirect(self):
        @self.app.route("/foo")
        def foo(request, response):
            response.text = "Foo"
            redirect("/bar")

        @self.app.route("/bar")
        def bar(request, response):
            response.text = "Bar"

        response = self.client.get("http://testserver/foo", allow_redirects=True)
        self.assertEqual(response.text, "Bar")
        orig_response = response.history[0]
        self.assertEqual(orig_response.status_code, 302)
        self.assertEqual(orig_response.url, "http://testserver/foo")

    def test_class_route(self):
        @self.app.route("/book/")
        class BookResource:
            def get(self, request, response):
                response.text = "Book page"

            def post(self, request, response):
                response.text = "Endpoint to create a book"

        response = self.client.get("http://testserver/book/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Book page")

        response = self.client.post("http://testserver/book/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Endpoint to create a book")

        response = self.client.delete("http://testserver/book/")
        self.assertEqual(response.status_code, 400)

        response = self.client.put("http://testserver/book/")
        self.assertEqual(response.status_code, 400)

        response = self.client.patch("http://testserver/book/")
        self.assertEqual(response.status_code, 400)

    def test_url_parameter(self):
        @self.app.route("/sync/{timestamp}")
        def sync(request, response, timestamp):
            response.text = f"Timestamp: {timestamp}"

        url = "http://testserver/sync/today"
        s = "Timestamp: today"
        self.assertEqual(self.client.get(url).text, s)

    def test_query_string(self):
        @self.app.route("/foo")
        def foo(request, response):
            response.text = f'color: {request.GET["color"]}'

        url = "http://testserver/foo?color=yellow"
        output = "color: yellow"
        self.assertEqual(self.client.get(url).text, output)

    def test_multiple_query_strings(self):
        @self.app.route("/foo")
        def foo(request, response):
            s = f'color: {request.GET["color"]} year: {request.GET["year"]}'
            response.text = s

        url = "http://testserver/foo?color=yellow&year=1987"
        output = "color: yellow year: 1987"
        self.assertEqual(self.client.get(url).text, output)

    def test_duplicate_route(self):
        @self.app.route("/home")
        def home(request, response):
            response.text = "Home page"

        self.assertTrue(self.app.routes["/home"] is home)

        with self.assertRaises(AssertionError):

            @self.app.route("/home")
            def second_home(request, response):
                response.text = "Second home page"

    def tearDown(self):
        logging.disable(logging.NOTSET)


class TestStaticFiles(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.WARNING)
        self.app = Drakken()
        self.client = Client(prefix="http://testserver", app=self.app)
        self.dir = tempfile.TemporaryDirectory()
        self.local_dir = tempfile.TemporaryDirectory(dir=os.getcwd())

    def test_absolute_path(self):
        path = os.path.join(self.dir.name, "hello.txt")
        with open(path, "wb") as f:
            f.write(b"Hello world")
        cfg = {"STATIC_DIR": self.dir.name}
        loads(cfg)

        url = f"http://testserver{path}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Hello world")

    def test_relative_path(self):
        path = os.path.join(self.local_dir.name, "hello.txt")
        with open(path, "wb") as f:
            f.write(b"Hello world")
        spath = os.path.split(self.local_dir.name)[1]
        cfg = {"STATIC_DIR": os.path.join("/", spath)}
        loads(cfg)

        url = os.path.join("http://testserver", spath, "hello.txt")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Hello world")

    def test_no_file(self):
        path = os.path.join(self.dir.name, "hello.txt")
        cfg = {"STATIC_DIR": self.dir.name}
        loads(cfg)

        url = f"http://testserver{path}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_directory(self):
        # Request for a directory. Written for production bugfix.
        path = os.path.join(self.dir.name, "my-dir")
        os.makedirs(path)
        cfg = {"STATIC_DIR": self.dir.name}
        loads(cfg)

        url = f"http://testserver{path}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_no_static_dir(self):
        cfg = {"STATIC_DIR": ""}
        loads(cfg)
        path = __file__
        url = f"http://testserver{path}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_out_of_bounds(self):
        # Request for a non-STATIC static file.
        path = __file__
        url = f"http://testserver{path}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_static_path(self):
        path = os.path.join(self.dir.name, "hello.txt")
        with open(path, "wb") as f:
            f.write(b"Hello world")
        cfg = {"STATIC_PATHS": [self.dir.name]}
        loads(cfg)

        url = f"http://testserver{path}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Hello world")

    def test_static_route_handler(self):
        # Serve static file using page controller.
        s = "Calm, steamy morning."
        path = os.path.join(self.dir.name, "hello.txt")
        with open(path, "w") as f:
            f.write(s)

        @self.app.route("/hello.txt")
        def hello(request, response):
            with open(path) as f:
                response.text = f.read()

        url = "http://testserver/hello.txt"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get(url).text, s)

    def tearDown(self):
        self.dir.cleanup()
        self.local_dir.cleanup()
        logging.disable(logging.NOTSET)
        cfg = {"STATIC_DIR": "/static"}
        loads(cfg)


class TestTrailingSlashRedirect(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.WARNING)
        self.app = Drakken()
        self.client = Client(prefix="http://testserver", app=self.app)
        cfg = {"TRAILING_SLASH_REDIRECT": True}
        loads(cfg)

    def test_trailing_slash(self):
        @self.app.route("/foo/")
        def foo(request, response):
            response.text = "Foo"

        response = self.client.get("http://testserver/foo/", allow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Foo")
        self.assertEqual(response.history, [])

        response = self.client.get("http://testserver/foo", allow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Foo")
        orig_response = response.history[0]
        self.assertEqual(orig_response.status_code, 301)
        self.assertEqual(orig_response.url, "http://testserver/foo")

    def test_no_trailing_slash(self):
        @self.app.route("/foo")
        def foo(request, response):
            response.text = "Foo"

        response = self.client.get("http://testserver/foo", allow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Foo")

        response = self.client.get("http://testserver/foo/", allow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Foo")
        orig_response = response.history[0]
        self.assertEqual(orig_response.status_code, 301)
        self.assertEqual(orig_response.url, "http://testserver/foo/")

    def tearDown(self):
        cfg = {"REDIRECT": False}
        loads(cfg)
        logging.disable(logging.NOTSET)


if __name__ == "__main__":
    unittest.main()
