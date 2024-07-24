"""Module for sending plain text emails."""

import logging
import smtplib
import traceback
from email.message import EmailMessage

from . import config
from .rate_limit import check_limit, OverLimit

logger = logging.getLogger(__name__)


def send(from_addr, to_addrs, subject, body):
    """Send email.

    Args:
        from_addr (str): sender email address.
        to_addrs (list): recipient email addresses.
        subject (str): email subject.
        body (str): email body.
    """
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = ", ".join(to_addrs)
    kwargs = dict(host=config.get("EMAIL_HOST"))
    if config.get("EMAIL_PORT"):
        kwargs["port"] = config.get("EMAIL_PORT")
    try:
        if config.get("EMAIL_REQUIRE_SSL"):
            server = smtplib.SMTP_SSL(**kwargs)
        else:
            server = smtplib.SMTP(**kwargs)
    except Exception:
        tb = traceback.format_exc()
        logger.error(f"SMTP exception {kwargs} {tb}")
        return
    username = config.get("EMAIL_HOST_USER")
    pw = config.get("EMAIL_HOST_PASSWORD")
    if username and pw:
        server.login(username, pw)
    try:
        server.send_message(msg)
        logger.info(f"sending email from: {from_addr} to: {to_addrs}")
    except smtplib.SMTPSenderRefused:
        logger.error(f"sender refused from: {from_addr} to: {to_addrs}")
    except smtplib.SMTPRecipientsRefused:
        logger.error(f"recipient refused from: {from_addr} to: {to_addrs}")
    server.quit()


def send_admins(subject, body):
    """Send email to ADMINS list from DEFAULT_FROM_EMAIL.

    Args:
        subject (str): email subject.
        body (str): email body.
    """
    from_addr = config.get("DEFAULT_FROM_EMAIL")
    to_addrs = config.get("ADMINS")
    try:
        limit = config.get("ADMIN_MAIL_LIMIT")
        unit = config.get("ADMIN_MAIL_UNIT")
        name = "send-admins"
        check_limit(limit, unit, name)
        send(from_addr, to_addrs, subject, body)
    except OverLimit as e:
        s = f"{name} rate limit exceeded: {limit} per {unit} count: {e}"
        logger.warning(s)
