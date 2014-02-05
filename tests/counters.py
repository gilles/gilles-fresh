# coding=utf-8
import unittest

import minimock

import counter


class CounterTest(unittest.TestCase):
    """
    Counter unit tests.
    These are based on what I know (minimock).
    Ideally GAE comes with mox / https://developers.google.com/appengine/docs/python/tools/localunittesting
    """

    def setUp(self):
        self.tt = minimock.TraceTracker()
        minimock.mock('counter.increment', tracker=self.tt)

    def tearDown(self):
        minimock.restore()

    def test_decorator_should_increment(self):
        @counter.counted('countername')
        def foo():
            pass

        foo()

        minimock.assert_same_trace(self.tt, '\n'.join([
            "Called counter.increment('countername')"
        ]))

    def test_decorator_should_increment_failed_and_raise(self):
        @counter.counted('countername')
        def foo():
            raise Exception('argh')

        self.assertRaises(Exception, foo)

        minimock.assert_same_trace(self.tt, '\n'.join([
            "Called counter.increment('countername_failed')"
        ]))

    def test_context_should_increment(self):
        with counter.counter('countername'):
            pass
        minimock.assert_same_trace(self.tt, '\n'.join([
            "Called counter.increment('countername')"
        ]))

    def test_context_should_increment_failed_and_raise(self):
        def foo():
            with counter.counter('countername'):
                raise Exception

        self.assertRaises(Exception, foo)
        minimock.assert_same_trace(self.tt, '\n'.join([
            "Called counter.increment('countername_failed')"
        ]))
