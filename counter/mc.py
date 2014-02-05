# coding=utf-8

from google.appengine.api import memcache
from google.appengine.ext import ndb

NAMESPACE = 'counter'


class NDBStorage(ndb.Model):
    count = ndb.IntegerProperty(default=0)


def increment(name, count=1):
    """
    Increment a counter
    TODO handle failure gracefully
    """
    memcache.incr(name, delta=count, initial_value=count, namespace=NAMESPACE)


def get_count(name):
    """
    Get count from the persistent storage
    """
    ndb_storage = NDBStorage.get_by_id(name, namespace=NAMESPACE)
    if ndb_storage is None:
        return 0
    return ndb_storage.count


def reap(counters):
    """
    Reap the counters from memcache and put them in persistent storage
    We need the increment/reset instead of get/put in case memcache fails (counter resetted to 0)

    This means that we loose the increments happening between the read and the set.
            We can use CAS to alleviate the problem but it won't make it go away for very busy counters
    """
    values = memcache.get_multi(counters, namespace=NAMESPACE)
    for key, value in values.iteritems():
        # we can use ndb.get_multi here to but handling the None is a bit more complex
        # it's possible but probably outside of the scope of the exercise
        ndb_storage = NDBStorage.get_by_id(key, namespace=NAMESPACE)
        if ndb_storage is None:
            ndb_storage = NDBStorage(id=key, namespace=NAMESPACE)
        ndb_storage.count += value
        ndb_storage.put()
        memcache.set(key, 0, namespace=NAMESPACE)
