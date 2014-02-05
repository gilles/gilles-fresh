#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

import jinja2
import webapp2

from counter import counted, counter
from counter.mc import reap, get_count


DECORATED_COUNTER = 'decorated'
CONTEXT_COUNTER = 'context'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


@counted(DECORATED_COUNTER)
def foo():
    """
    Decorated function, add you logic in there
    """
    pass


class MainHandler(webapp2.RequestHandler):
    def get(self):
        counters = {
            'decorated': get_count(DECORATED_COUNTER),
            'context': get_count(CONTEXT_COUNTER)
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'counters': counters}))

    def post(self):
        # decorated
        foo()
        # context
        with counter(CONTEXT_COUNTER):
            # your logic here
            pass
        self.response.set_status(201)


def trigger_reap(request, *args, **kwargs):
    """
    This should be protected so it's not accessible to the public:
    https://developers.google.com/appengine/docs/python/config/cron#Python_app_yaml_Securing_URLs_for_cron
    """
    reap([DECORATED_COUNTER, CONTEXT_COUNTER])
    counters = {
        'decorated': get_count(DECORATED_COUNTER),
        'context': get_count(CONTEXT_COUNTER)
    }
    template = JINJA_ENVIRONMENT.get_template('index.html')
    return webapp2.Response(template.render({'counters': counters}))


app = webapp2.WSGIApplication(
    [
        ('/', MainHandler),
        ('/reap', trigger_reap),
    ], debug=True)
