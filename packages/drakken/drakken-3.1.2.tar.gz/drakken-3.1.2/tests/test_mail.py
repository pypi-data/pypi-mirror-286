"""Test harness for drakken.mail.

unittest.mock was too complex. MockSMTP is simple: was an email sent?
"""

import logging
import smtplib
import unittest

from drakken.config import loads
from drakken.core import Drakken
from drakken.mail import send, send_admins
from drakken.mock import Client
from drakken.model import setup


class MockSMTP:
    instances = []

    def __init__(self, host="", port=0):
        self.host = host
        self.port = port
        self.outbox = []
        MockSMTP.instances.append(self)

    def login(self, user, password):
        self.user = user
        self.password = password

    def send_message(self, msg):
        self.outbox.append(msg)

    def quit(self):
        self.has_quit = True


smtplib.SMTP = MockSMTP


class TestMail(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.ERROR)
        setup()

    def test_send_localhost(self):
        sender = "drakken@gmail.com"
        recipient = "anybody@gmail.com"
        subject = "Hello"
        body = "This is my body\n"

        cfg = {
            "EMAIL_HOST": "localhost",
            "EMAIL_PORT": None,
            "EMAIL_HOST_USER": "",
            "EMAIL_HOST_PASSWORD": "",
        }
        loads(cfg)

        send(sender, [recipient], subject, body)
        server = MockSMTP.instances.pop()
        self.assertEqual(len(server.outbox), 1)
        msg = server.outbox[0]
        self.assertEqual(msg["To"], recipient)
        self.assertEqual(msg["From"], sender)
        self.assertEqual(msg["Subject"], subject)
        self.assertEqual(msg.get_payload(), body)
        self.assertEqual(server.host, "localhost")
        self.assertEqual(server.port, 0)
        self.assertTrue(server.has_quit)

    def test_send_with_login(self):
        sender = "drakken@gmail.com"
        recipient = "anybody@gmail.com"
        subject = "Hello"
        body = "This is my body\n"

        cfg = {
            "EMAIL_HOST": "myhost",
            "EMAIL_PORT": 997,
            "EMAIL_HOST_USER": "my-user-name",
            "EMAIL_HOST_PASSWORD": "my-password",
        }
        loads(cfg)

        send(sender, [recipient], subject, body)
        server = MockSMTP.instances.pop()
        self.assertEqual(len(server.outbox), 1)
        msg = server.outbox[0]
        self.assertEqual(msg["To"], recipient)
        self.assertEqual(msg["From"], sender)
        self.assertEqual(msg["Subject"], subject)
        self.assertEqual(msg.get_payload(), body)
        self.assertEqual(server.host, "myhost")
        self.assertEqual(server.port, 997)
        self.assertEqual(server.user, "my-user-name")
        self.assertEqual(server.password, "my-password")
        self.assertTrue(server.has_quit)

    def test_send_admin(self):
        recipient = "admin-email-address"
        sender = "server-address"
        subject = "my-email-subject"

        cfg = {
            "EMAIL_HOST": "localhost",
            "EMAIL_PORT": None,
            "EMAIL_HOST_USER": "",
            "EMAIL_HOST_PASSWORD": "",
            "ADMINS": [recipient],
            "DEFAULT_FROM_EMAIL": sender,
        }
        loads(cfg)

        body = "This is my body\n"
        send_admins(subject, body)

        server = MockSMTP.instances.pop()
        self.assertEqual(len(server.outbox), 1)
        msg = server.outbox[0]
        self.assertEqual(msg["To"], recipient)
        self.assertEqual(msg["From"], sender)
        self.assertEqual(msg["Subject"], subject)
        self.assertEqual(msg.get_payload(), body)
        self.assertEqual(server.host, "localhost")
        self.assertEqual(server.port, 0)
        self.assertTrue(server.has_quit)

    def tearDown(self):
        logging.disable(logging.NOTSET)


class TestServerError(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.ERROR)
        self.app = Drakken()
        self.client = Client(prefix="http://testserver", app=self.app)

    def test_email_on_error(self):
        recipient = "admin-email-address"
        sender = "server-address"
        subject = "Drakken mail test server error"

        cfg = {
            "EMAIL_HOST": "localhost",
            "EMAIL_PORT": None,
            "EMAIL_HOST_USER": "",
            "EMAIL_HOST_PASSWORD": "",
            "APP_NAME": "Drakken mail test",
            "ADMINS": [recipient],
            "DEFAULT_FROM_EMAIL": sender,
        }
        loads(cfg)

        @self.app.route("/home")
        def home(request, response):
            raise KeyError
            response.text = "Calm, steamy morning."

        url = "http://testserver/home"
        self.assertEqual(self.client.get(url).status_code, 500)

        server = MockSMTP.instances.pop()
        self.assertEqual(len(server.outbox), 1)
        msg = server.outbox[0]
        self.assertEqual(msg["To"], recipient)
        self.assertEqual(msg["From"], sender)
        self.assertEqual(msg["Subject"], subject)
        self.assertTrue("Traceback" in msg.get_payload())
        self.assertTrue("KeyError" in msg.get_payload())
        self.assertTrue(server.has_quit)

    def tearDown(self):
        logging.disable(logging.NOTSET)


if __name__ == "__main__":
    unittest.main()
