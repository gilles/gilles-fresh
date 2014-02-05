# coding=utf-8

from google.appengine.api import memcache
from google.appengine.ext import ndb

NAMESPACE = 'counter'

# I doubt this will grow out of proportions even with
# dynamic counters
_counter_cache = set()


class NDBStorage(ndb.Model):
    count = ndb.IntegerProperty(default=0)


@ndb.transactional
def track_counter(name):
    ndb_storage = NDBStorage.get_by_id(name, namespace=NAMESPACE)
    if ndb_storage is None:
        ndb_storage = NDBStorage(id=name, namespace=NAMESPACE)
        ndb_storage.put()


def increment(name, count=1):
    """
    Increment a counter
    TODO handle failure gracefully
    """
    # check the counter is tracked
    if name not in _counter_cache:
        track_counter(name)
        _counter_cache.add(name)
    print 'increment: %s' % name
    memcache.incr(name, delta=count, initial_value=0, namespace=NAMESPACE)


def get_count(name):
    """
    Get count from the persistent storage
    """
    ndb_storage = NDBStorage.get_by_id(name, namespace=NAMESPACE)
    if ndb_storage is None:
        return 0
    return ndb_storage.count


def get_all_counters():
    return NDBStorage.query(namespace=NAMESPACE).iter()


@ndb.transactional
def _increment_db(record, value):
    record.count += value
    record.put()


def reap():
    """
    Reap the counters from memcache and put them in persistent storage
    We need the increment/reset instead of get/put in case memcache fails (counter resetted to 0)
    """

    # This might be more efficient by paginating manually and do memcache.get_multi
    for counter in get_all_counters():
        value = memcache.get(counter.key.string_id(), namespace=NAMESPACE)
        # if value is None:
        #     continue
        _increment_db(counter, value)
        memcache.decr(counter.key.string_id(), value, namespace=NAMESPACE)
        print 'memcache: %s => %s' % (counter.key.string_id(), memcache.get(counter.key.string_id(), namespace=NAMESPACE))
