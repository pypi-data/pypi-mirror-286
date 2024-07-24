"""Rate limit module."""

from sqlalchemy import select

from datetime import datetime, timedelta
from functools import wraps
import logging

from . import config
from . import model

logger = logging.getLogger(__name__)


class OverLimit(Exception):
    """The number of requests exceeds the limit."""

    pass


def check_limit(limit, unit, name="default"):
    """Increment count and compare to limit.

    Args:
        limit (int): max number of executions.
        unit (str): 'SECOND', 'MINUTE', 'HOUR', 'DAY'.
        name (str): limiter name. Default is 'default'.

    Raises:
        OverLimit: number of calls is over the limit.

    Uses a fixed window rate length algorithm:

    1. On the first call, store the datetime and the count (1).
    2. On subsequent calls, check the datetime: if the time window has expired, store the new datetime and reset the count to (1).
    3. If the window hasn't expired, increment and store the count.
    4. If the count is over the limit, raise OverLimit exception.

    Example::

        from drakken.rate_limit import check_limit, OverLimit
        limit = 12
        unit = 'MINUTE'
        try:
            check_limit(limit=limit, unit=unit)
        except OverLimit as e:
            s = f'Rate limit exceeded: {limit} per {unit} count: {e}'
            logger.warning(s)
    """
    with model.session_scope() as session:
        q = select(model.RateLimit).where(model.RateLimit.name == name)
        limiter = session.scalars(q).first()
        if not limiter:
            limiter = model.RateLimit(name=name, start_time=datetime.now(), count=1)
            session.add(limiter)
            return
        limiter.count += 1
        delta = timedelta(**{unit.lower() + "s": 1})
        # If time expired, reset.
        if datetime.now() > limiter.start_time + delta:
            limiter.start_time = datetime.now()
            limiter.count = 1
        elif limiter.count > limit:
            raise OverLimit(limiter.count)


def rlimit(limit, unit, name="default"):
    """Rate limit decorator that calls `check_limit()`.

    Args:
        limit (int): max number of executions.
        unit (str): 'SECOND', 'MINUTE', 'HOUR', 'DAY'.
        name (str): limiter name. Default is 'default'.

    If the rate limit is exceeded the decorated function isn't executed.

    Example::

        import drakken.rate_limit as rlimit

        @rlimit.rlimit(limit=3, unit='SECOND')
        def sum(x, y):
            return x + y

        z = sum(4, 3)   # 1
        z = sum(12, 1)  # 2
        z = sum(6, 2)   # 3
        z = sum(9, 5)   # Over limit
    """

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                check_limit(limit, unit, name)
            except OverLimit as e:
                s = f"Rate limit exceeded: {limit} per {unit} count: {e}"
                logger.warning(s)
                return None
            res = function(*args, **kwargs)
            return res

        return wrapper

    return decorator
