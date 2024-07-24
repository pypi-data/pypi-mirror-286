from datetime import datetime, timedelta
import logging
import unittest

from sqlalchemy import select

import drakken.model as model
import drakken.rate_limit as rlimit


class TestRateLimit(unittest.TestCase):
    def setUp(self):
        model.setup()

    def test_limit_reached(self):
        limit = 3

        @rlimit.rlimit(limit, "SECOND")
        def sum(x, y):
            sum.counter += 1
            return x + y

        sum.counter = 0

        # 1
        z = sum(4, 3)
        self.assertEqual(z, 7)
        self.assertEqual(sum.counter, 1)
        # 2
        z = sum(12, 1)
        self.assertEqual(z, 13)
        self.assertEqual(sum.counter, 2)
        # 3
        z = sum(6, 2)
        self.assertEqual(z, 8)
        self.assertEqual(sum.counter, 3)

        # Function not executed, warning logged.
        with self.assertLogs(logger="drakken.rate_limit", level="INFO") as lc:
            z = sum(9, 5)
        self.assertTrue("Rate limit exceeded" in lc.output[0])
        self.assertEqual(sum.counter, 3)

    def test_time_expired(self):
        limit = 100

        @rlimit.rlimit(limit, "SECOND")
        def sum(x, y):
            sum.counter += 1
            return x + y

        sum.counter = 0

        # Execute function.
        z = sum(4, 5)
        self.assertEqual(z, 9)
        self.assertEqual(sum.counter, 1)
        z = sum(1, 7)
        self.assertEqual(z, 8)
        self.assertEqual(sum.counter, 2)
        # Set db.start_time to expired.
        q = select(model.RateLimit)
        with model.session_scope() as session:
            limiter = session.scalars(q).one()
            limiter.count = 50
            limiter.start_time = datetime.now() - timedelta(minutes=5)
        z = sum(1, 2)
        self.assertEqual(z, 3)
        self.assertEqual(sum.counter, 3)
        # Expired time limit resets counter.
        with model.session_scope() as session:
            limiter = session.scalars(q).one()
        self.assertEqual(limiter.count, 1)

    def test_multiple_limiters(self):
        limit_sum = 3
        limit_upper = 5

        @rlimit.rlimit(limit_sum, "SECOND", name="sum")
        def sum(x, y):
            sum.counter += 1
            return x + y

        sum.counter = 0

        @rlimit.rlimit(limit_upper, "SECOND", name="upper")
        def upper(s):
            upper.counter += 1
            return s.upper()

        upper.counter = 0

        # 1
        z = sum(4, 3)
        self.assertEqual(z, 7)
        self.assertEqual(sum.counter, 1)
        # 2
        z = sum(12, 1)
        self.assertEqual(z, 13)
        self.assertEqual(sum.counter, 2)
        # 3
        z = sum(4, 5)
        self.assertEqual(z, 9)
        self.assertEqual(sum.counter, 3)

        # Function not executed, warning logged.
        with self.assertLogs(logger="drakken.rate_limit", level="INFO") as lc:
            z = sum(9, 5)
        self.assertTrue("Rate limit exceeded" in lc.output[0])
        self.assertEqual(sum.counter, 3)

        # 1
        s = upper("hello")
        self.assertEqual(s, "HELLO")
        self.assertEqual(upper.counter, 1)
        # 2
        s = upper("goodbye")
        self.assertEqual(s, "GOODBYE")
        self.assertEqual(upper.counter, 2)
        # 3
        s = upper("morning")
        self.assertEqual(s, "MORNING")
        self.assertEqual(upper.counter, 3)
        # 4
        s = upper("evening")
        self.assertEqual(s, "EVENING")
        self.assertEqual(upper.counter, 4)
        # 5
        s = upper("today")
        self.assertEqual(s, "TODAY")
        self.assertEqual(upper.counter, 5)

        # Function not executed, warning logged.
        with self.assertLogs(logger="drakken.rate_limit", level="INFO") as lc:
            s = upper("day")
        self.assertTrue("Rate limit exceeded" in lc.output[0])
        self.assertEqual(upper.counter, 5)

    def test_one_limiter_multiple_functions(self):
        limit = 5

        @rlimit.rlimit(limit, "SECOND")
        def sum(x, y):
            sum.counter += 1
            return x + y

        sum.counter = 0

        @rlimit.rlimit(limit, "SECOND")
        def upper(s):
            upper.counter += 1
            return s.upper()

        upper.counter = 0

        # 1
        z = sum(4, 3)
        self.assertEqual(z, 7)
        self.assertEqual(sum.counter, 1)
        # 2
        s = upper("hello")
        self.assertEqual(s, "HELLO")
        self.assertEqual(upper.counter, 1)
        # 3
        z = sum(4, 5)
        self.assertEqual(z, 9)
        self.assertEqual(sum.counter, 2)
        # 4
        s = upper("goodbye")
        self.assertEqual(s, "GOODBYE")
        self.assertEqual(upper.counter, 2)
        # 5
        z = sum(4, 5)
        self.assertEqual(z, 9)
        self.assertEqual(sum.counter, 3)

        # Function not executed, warning logged.
        with self.assertLogs(logger="drakken.rate_limit", level="INFO") as lc:
            s = upper("day")
        self.assertTrue("Rate limit exceeded" in lc.output[0])
        self.assertEqual(upper.counter, 2)


if __name__ == "__main__":
    unittest.main()
