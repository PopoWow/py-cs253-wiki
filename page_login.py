import os

from google.appengine.ext import db

from pagebase import BaseApp, BaseHandler
import utils
from urls import *
from model_user import User


class LoginHandler(BaseHandler): 
    def get(self):
        if self.user:
            self.redirect(URL_ROOT)
        else:
            vdata = {}
            self.render('login_form.html', vdata=vdata)
    
    def post(self):
        username = self.request.get('username').lower()
        password = self.request.get('password')
        vdata = dict(self.request.params)
        
        submit_error = False
        if not username:
            vdata['e_username'] = "Please enter a username"
            submit_error = True
        if not password:
            vdata['e_password'] = "Please enter a password"
            submit_error = True
            
        if submit_error:
            self.render('login_form.html', vdata=vdata)
        else:
            # No form submit errors.  Query for the user
            user_rec = User.by_username(username)

            if user_rec and utils.valid_pw_hash(username, password, user_rec.pw_hash):
                # found the username and the salt checked out!
                self.login(user_rec)
                self.redirect(URL_ROOT)
            else:
                vdata['e_login'] = "Invalid Login"
                self.render('login_form.html', vdata=vdata)

class LogoutHandler(BaseHandler):
    def get(self):
        self.logout()
        self.redirect(URL_LOGIN)


