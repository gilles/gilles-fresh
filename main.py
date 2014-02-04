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
import webapp2

from counter import counted, counter
from counter.db import get_count


DECORATED_COUNTER = 'decorated'
CONTEXT_COUNTER = 'context'


@counted(DECORATED_COUNTER)
def foo():
    """
    Decorated function, add you logic in there
    """
    pass


class MainHandler(webapp2.RequestHandler):
    def get(self):
        decorated = get_count(DECORATED_COUNTER)
        context = get_count(CONTEXT_COUNTER)
        # TODO move this in a template
        self.response.write('<html><body><h1>%s: %d</h1><h1>%s: %d</h1></body></html>' %
                            (DECORATED_COUNTER, decorated, CONTEXT_COUNTER, context)
        )

    def post(self):
        # decorated
        foo()
        # context
        with counter(CONTEXT_COUNTER):
            # your logic here
            pass
        self.response.set_status(201)


app = webapp2.WSGIApplication(
    [
        ('/', MainHandler)
    ], debug=True)
