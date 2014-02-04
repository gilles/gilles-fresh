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
* No unit tests
* No templates
* Can't get siege to work to test concurrency GAE returns 500 (can use curl and Postman though)
