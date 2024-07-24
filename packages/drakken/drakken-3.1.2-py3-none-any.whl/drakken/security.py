"""Session security module."""

import hashlib
import secrets

from . import config


def create_CSRF_token():
    """Create CSRF token.

    Returns:
        str: CSRF token.
    """
    return secrets.token_urlsafe(config.get("CSRF_TOKEN_BYTES"))


def create_session_cookie(token, path="/"):
    """Create session cookie from token string.

    To close session when browser closes, set SESSION_COOKIE_AGE = 0.

    Args:
        token (str): unique session ID.
        path (str): requested URL must have this path to send the cookie.

    Returns:
        dict: For Response.set_cookie().
    """
    cookie = dict(
        name="sessionid",
        value=token,
        path=path,
        secure=config.get("SESSION_COOKIE_SECURE"),
        httponly=True,
        samesite="strict",
    )
    age = config.get("SESSION_COOKIE_AGE")
    if age:
        cookie["max_age"] = age
    return cookie


def create_session_token():
    """Create session token aka session ID.

    Returns:
        str: Session token.
    """
    return secrets.token_urlsafe(config.get("SESSION_TOKEN_BYTES"))


def gensalt():
    """Create salt.

    Returns:
        str: Password salt.
    """
    return secrets.token_urlsafe(config.get("SALT_BYTES"))


def fast_hash(s):
    """Hash string s using SHA256.

    Use on session IDs etc where speed is essential.

    Args:
        s (str): string to be hashed.

    Returns:
        str: Hashed input string.
    """
    return hashlib.sha256(s.encode()).hexdigest()


def slow_hash(s, salt):
    """Hash string s with salt.

    Use on passwords and password reset tokens before storing in the
    database. It's slow so don't use on session IDs.

    Note:
        Uses scrypt to thwart password cracking hardware.
        n,r,p values suggested by OWASP.

    Args:
        s (str): string to be hashed.
        salt (str): random string added to input string.

    Returns:
        bytes: Hashed input string.
    """
    return hashlib.scrypt(password=s.encode(), salt=salt.encode(), n=16384, r=8, p=1)


def verify(s, salt, h):
    """Return True if string slow-hashed with salt matches hash.

    Args:
        s (str): string to be tested.
        salt (str): random string added to input string.
        h (bytes): hash bytes.

    Returns:
        bool: True if string + salt matches hash.
    """
    return slow_hash(s, salt) == h
