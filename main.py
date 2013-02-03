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
#import webapp2
from urls import *
from pagebase import BaseApp, BaseHandler
from page_signup import SignupHandler
from page_login import LoginHandler, LogoutHandler
from page_view import ViewHandler
from page_edit import EditHandler
from page_history import HistoryHandler

class MainHandler(BaseHandler):
    def get(self):
        self.response.write('Hello world!')

app = BaseApp([(URL_SIGNUP,     SignupHandler),
               (URL_LOGIN,      LoginHandler),
               (URL_RE_LOGOUT,  LogoutHandler),
               (URL_RE_HIST,    HistoryHandler),
               (URL_RE_EDIT,    EditHandler),
               (URL_VIEW,       ViewHandler)                           
               ],
               debug=True)
