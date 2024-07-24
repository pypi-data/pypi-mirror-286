"""Template module."""

import json
import os
from types import SimpleNamespace

from mako.template import Template
from mako.lookup import TemplateLookup
import sqlalchemy

from . import config
from .exceptions import LoginFail
import drakken.model as model
import drakken.security as security


def _create_CSRF_input(csrf_token, ip_address, user_agent):
    """Create CSRF token and store in session table.

    Args:
        csrf_token (str): CSRF token.
        ip_address (str): request IP address.
        user_agent (str): request user agent.

    Returns:
        str: CSRF token.
    """
    if not csrf_token:
        csrf_token = security.create_CSRF_token()
        with model.session_scope() as sql_session:
            session = model.Session(
                csrf_token=csrf_token,
                ip_address=ip_address,
                user_agent=user_agent,
            )
            sql_session.add(session)
    return csrf_token


def _get_static_path():
    """Return static file path from config.STATIC_DIR."""
    return config.get("STATIC_DIR")


def render(request, template, context={}):
    """Render template and return as string.

    Args:
        request (Request): Request object.
        template (str): path to template in config.TEMPLATE_DIR.
        context (dict): objects to load into template.

    Returns:
        str: HTML rendered from template.
    """
    try:
        session = model.get_session(request)
        user = session.user
        csrf_token = session.csrf_token
    except (LoginFail, sqlalchemy.exc.UnboundExecutionError):
        # No db connection detected. Allows Drakken to be used without a db.
        user = SimpleNamespace(is_authenticated=False)
        csrf_token = None
    context["user"] = user
    path = os.path.join(config.get("TEMPLATE_DIR"), template)
    lookup = TemplateLookup(directories=[os.getcwd()])
    t = Template(filename=path, lookup=lookup)
    context["STATIC"] = _get_static_path()
    # Generate CSRF token only if called for in template.
    if "${CSRF}" in t.source:
        context["CSRF"] = _create_CSRF_input(
            csrf_token=csrf_token,
            ip_address=request.client_addr,
            user_agent=request.user_agent,
        )
    return t.render(**context)


def read(path):
    """Read file and return contents.

    Args:
        path (str): file path from config.TEMPLATE_DIR.

    Returns:
       str if a text file, dict if a json file.
    """
    path = os.path.join(config.get("TEMPLATE_DIR"), path)
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError:
            return f.read()
