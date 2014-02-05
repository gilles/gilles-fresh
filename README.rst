APP ENGINE
==========

What's there
------------

This is a first pass to make counters in the app engine.
It's using https://developers.google.com/appengine/articles/sharding_counters from the google developer center.

It's easy to count things via a decorator and a context manager.

It is very basic, just has the root endpoint:

* `GET /` => display the two predetermined counters
* `POST /` => Increment the two test counters

It lives here: http://gilles-freshplanet.appspot.com/

Limitations and TODO
--------------------

* Increment by 1 only (should be easy to add)
* Can't get siege to work to test concurrency GAE returns 500 (can use curl and Postman though)

Depensing on GAE pricing structure, incrementing all these keys in NDB might get expensive. One alternative
solution could be to increment in memcache (possibly sharded but dedicated memcache are advertised as 10k ops/s)
and have reaper (cron) jobs get the value, increment NDB then clear the memcache counter.

You might tolerate some data loss (if memcache goes down) or handle it gracefully by putting the action in a log and replay it.
