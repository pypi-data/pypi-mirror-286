"""Configuration module using `pyaml` library.

Supports JSON and YAML config file formats.
"""

import yaml


def get(key):
    """Return configuration value for this key.

    Args:
        key (str): config dictionary key.

    Returns:
        str: value for this key.
    """
    return config[key]


def loads(d):
    """Load dictionary d into config.

    Args:
        d (dict): configuration dictionary.
    """
    config.update(d)


def load(path):
    """Load config file into this app's configuration.

    Args:
        path (str): file path.
    """
    with open(path, "r") as f:
        d = yaml.safe_load(f)
    config.update(d)


# Default values.
config = {
    "APP_NAME": "Drakken app",  # Used for logging.
    "LOGIN_URL": "",
    "USERNAME": False,
    "STATIC_DIR": "/static",
    "STATIC_PATHS": [],
    "TEMPLATE_DIR": "templates",
    "TRAILING_SLASH_REDIRECT": False,
    "DEBUG": False,
    # Sessions
    "SESSION_COOKIE_SECURE": False,
    "DATABASE_URL": "sqlite:///demo.sqlite3",
    "SESSION_COOKIE_AGE": 86400,  # Sessions last 1 day.
    "CSRF_TOKEN_BYTES": 16,
    "SALT_BYTES": 16,
    "SESSION_TOKEN_BYTES": 16,
    # Per OWASP: min password length: 8, max password length: 64 to
    # prevent password DOS attacks.
    "MIN_PASSWORD_LENGTH": 8,
    "MAX_PASSWORD_LENGTH": 64,
    # Email
    "EMAIL_HOST": "localhost",
    "EMAIL_PORT": None,
    "EMAIL_REQUIRE_SSL": False,
    "EMAIL_HOST_USER": "",
    "EMAIL_HOST_PASSWORD": "",
    "DEFAULT_FROM_EMAIL": "drakken@localhost",
    "ADMINS": [],
    # Email rate limit
    "ADMIN_MAIL_LIMIT": 100,
    "ADMIN_MAIL_UNIT": "DAY",
}
