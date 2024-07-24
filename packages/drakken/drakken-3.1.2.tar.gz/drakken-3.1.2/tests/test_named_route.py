import os
import tempfile
import unittest

from drakken.core import Drakken, Blueprint
from drakken.mock import Client
from drakken.template import render


class TestURLNameParser(unittest.TestCase):
    def setUp(self):
        self.app = Drakken()

    def test_parse_url_names(self):
        p1 = "/account/howdy/"
        p2 = "/account/hello/"

        s = "blah {% url howdy %} blah {% url hello %} blah"
        s1 = "blah /account/howdy/ blah {% url hello %} blah"
        s2 = "blah {% url howdy %} blah /account/hello/ blah"
        self.assertEqual(self.app._get_url_names(s), ["howdy", "hello"])
        self.assertEqual(self.app._replace_url_name("howdy", p1, s), s1)
        self.assertEqual(self.app._replace_url_name("hello", p2, s), s2)

        s = "blah {%url howdy %} blah {% url hello%} blah"
        s1 = "blah /account/howdy/ blah {% url hello%} blah"
        s2 = "blah {%url howdy %} blah /account/hello/ blah"
        self.assertEqual(self.app._get_url_names(s), ["howdy", "hello"])
        self.assertEqual(self.app._replace_url_name("howdy", p1, s), s1)
        self.assertEqual(self.app._replace_url_name("hello", p2, s), s2)

        s = "blah {% urlhowdy %} blah {% url hello %} blah"
        s2 = "blah {% urlhowdy %} blah /account/hello/ blah"
        self.assertEqual(self.app._get_url_names(s), ["hello"])
        self.assertEqual(self.app._replace_url_name("hello", p2, s), s2)

        s = "blah {%   url    howdy   %} blah {%   url   hello        %} blah"
        s1 = "blah /account/howdy/ blah {%   url   hello        %} blah"
        s2 = "blah {%   url    howdy   %} blah /account/hello/ blah"
        self.assertEqual(self.app._get_url_names(s), ["howdy", "hello"])
        self.assertEqual(self.app._replace_url_name("howdy", p1, s), s1)
        self.assertEqual(self.app._replace_url_name("hello", p2, s), s2)


class TestLoadNamedRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Drakken()

    def test_single_url(self):
        @self.app.route("/hello/", name="howdy")
        def a(request, response):
            response.text = "hello"

        s = "<html><p>Hello</p>{% url howdy %}</html>"
        converted = "<html><p>Hello</p>/hello/</html>"
        html = self.app._load_named_routes(s)
        self.assertEqual(html, converted)

    def test_repeat_url(self):
        @self.app.route("/hello/", name="howdy")
        def a(request, response):
            response.text = "hello"

        s = """<html><p>Hello</p><a href={% url howdy %}</a>
        <p>This is more text</p><a href={% url howdy %}</a></html>"""
        converted = """<html><p>Hello</p><a href=/hello/</a>
        <p>This is more text</p><a href=/hello/</a></html>"""
        html = self.app._load_named_routes(s)
        self.assertEqual(html, converted)

    def test_multiple_urls(self):
        @self.app.route("/hello/", name="howdy")
        def a(request, response):
            response.text = "hello"

        @self.app.route("/goodbye/", name="adios")
        def b(request, response):
            response.text = "goodbye"

        @self.app.route("/wait/", name="wait")
        def c(request, response):
            response.text = "wait"

        s = "blah {% url howdy %} blah {% url adios %} blah {% url wait %} blah blah"
        converted = "blah /hello/ blah /goodbye/ blah /wait/ blah blah"
        html = self.app._load_named_routes(s)
        self.assertEqual(html, converted)

    def test_blueprints(self):
        account = Blueprint(name="account", url_prefix="/customer-account")
        settings = Blueprint(name="settings", url_prefix="/customer-settings")

        @account.route("/login/", name="howdy")
        def a(request, response):
            response.text = "login"

        @account.route("/create/", name="adios")
        def b(request, response):
            response.text = "create"

        @settings.route("/orders/", name="purchases")
        def c(request, response):
            response.text = "orders"

        self.app.register_blueprint(account)
        self.app.register_blueprint(settings)

        s = "blah {% url howdy %} blah {% url adios %} blah {% url purchases %} blah blah"
        converted = "blah /customer-account/login/ blah /customer-account/create/ blah /customer-settings/orders/ blah blah"
        html = self.app._load_named_routes(s)
        self.assertEqual(html, converted)


class TestNamedRouteResponse:
    def setUp(self):
        self.app = Drakken()
        self.client = Client(prefix="http://testserver", app=self.app)
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, "test.html")

    def test_html(self):
        html = "<html><p>{% url adios %}</p></html>"
        with open(self.path, "w") as f:
            f.write(html)

        @self.app.route("/goodbye", name="adios")
        def goodbye(request, response):
            response.text = "See you later"

        @self.app.route("/hello")
        def hello(request, response):
            response.text = render(request, self.path)

        r = self.client.get("http://testserver/hello")
        self.assertTrue("<p>/goodbye</p>" in r.text)

    def tearDown(self):
        self.dir.cleanup()


if __name__ == "__main__":
    unittest.main()
