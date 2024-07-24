import logging
import unittest

from drakken.core import Drakken
from drakken.middleware import CSRFMiddleware, Middleware
from drakken.mock import Client
from drakken.model import setup
from drakken.config import loads


cfg = {
    "DATABASE_URL": "sqlite:///:memory:",
}
loads(cfg)


class TestMiddleware(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.WARNING)
        self.app = Drakken()
        self.client = Client(prefix="http://testserver", app=self.app)
        setup()

        @self.app.route("/")
        def home(request, response):
            response.text = "Hello"

    def test_1_middleware(self):
        class M1(Middleware):
            def process_response(self, request, response):
                response.text += " world."

        self.app.add_middleware(M1)
        response = self.client.get(url="http://testserver/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Hello world.")

    def test_2_middleware(self):
        class M1(Middleware):
            def process_response(self, request, response):
                response.text += " world."

        class M2(Middleware):
            def process_response(self, request, response):
                response.text += " Beautiful day!"

        self.app.add_middleware(M1)
        self.app.add_middleware(M2)
        response = self.client.get(url="http://testserver/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Hello world. Beautiful day!")

    def tearDown(self):
        logging.disable(logging.NOTSET)


class TestCSRFMiddleware(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.WARNING)
        self.app = Drakken()
        self.app.add_middleware(CSRFMiddleware)
        self.client = Client(prefix="http://testserver", app=self.app)
        setup()

        @self.app.route("/")
        def home(request, response):
            response.text = "Hello"

    def test_delete(self):
        response = self.client.delete(
            url="http://testserver/",
            data=dict(fake="fake-data"),
        )
        self.assertEqual(response.status_code, 403)

    def test_get(self):
        response = self.client.get(url="http://testserver/")
        self.assertEqual(response.status_code, 200)

    def test_patch(self):
        response = self.client.patch(
            url="http://testserver/",
            data=dict(fake="fake-data"),
        )
        self.assertEqual(response.status_code, 403)

    def test_post(self):
        response = self.client.post(
            url="http://testserver/",
            data=dict(fake="fake-data"),
        )
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        response = self.client.put(
            url="http://testserver/",
            data=dict(fake="fake-data"),
        )
        self.assertEqual(response.status_code, 403)

    def tearDown(self):
        logging.disable(logging.NOTSET)


if __name__ == "__main__":
    unittest.main()
