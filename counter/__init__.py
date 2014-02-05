# coding=utf-8
from contextlib import contextmanager
from functools import wraps

from counter.mc import increment


def counted(counter_name):
    """
    decorator for easy counting.
    This makes an assumption that failure comes from an exception only.
        The behaviour could be augmented by passing failure return type/values to check for in the args
    """

    def wrap(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                ret = f(*args, **kwargs)
                increment(counter_name)
            except Exception:
                increment(counter_name + '_failed')
                raise
            return ret

        return wrapper

    return wrap


@contextmanager
def counter(counter_name):
    """
    A simple context manager to inncrement a counter
    """
    try:
        yield
    except Exception:
        increment(counter_name + '_failed')
        raise
    increment(counter_name)
