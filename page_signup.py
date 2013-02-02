import os

from google.appengine.ext import db

from pagebase import BaseApp, BaseHandler
import utils
from urls import *
from model_user import User

class SignupHandler(BaseHandler):
    def get(self):
        vdata = dict(self.request.params)
        self.render('signup_form.html', vdata=vdata)
        
    def post(self):
        
        # NOTES: this kind of technique I'm using won't scale well.  Need to
        # transition to a system where a dict is contructed dynmically.
        
        username = self.request.get('username').lower()
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        
        vdata = dict(self.request.params)
        
        submit_error = False
        if not utils.valid_username(username):
            vdata['e_username'] = "That's not a valid username."
            submit_error = True
            
        if utils.valid_password(password):
            if password != verify:
                vdata['e_verify'] = "Your passwords didn't match."
                submit_error = True
        else:
            vdata['e_password'] = "That wasn't a valid password."
            submit_error = True
            
        if not utils.valid_email(email):
            vdata['e_email'] = "That's not a valid email."
            submit_error = True
        
        if submit_error:
            self.render('signup_form.html', vdata=vdata)
        else:
            #form filled out successfully, check DB for dupes            
            user_rec = User.by_username(username)
            if user_rec:
                # dupe!!!
                vdata['e_username'] = "That user already exists."
                self.render('signup_form.html', vdata=vdata)
            else:
                # sign up form was successful.  Now, first create a password
                # hash and create a Users entity.
                new_user = User.register(username, password, email)
                new_user.put()
                
                # now we want to store a cookie indicating a user.  send
                # the "Set-Cookie" data in the redirect response :)
                user_id = new_user.key().id()
                self.set_secure_cookie('user_id', user_id)
                self.redirect(URL_ROOT)

class WelcomePage(BaseHandler):
    def get(self):
        username = "User"
        user_hash = self.request.cookies.get('user_id')
        if user_hash:
            user_id = utils.valid_cookie_hash(user_hash)
            if user_id and user_id.isdigit():
                user_obj = model_users.Users.get_by_id(int(user_id))
                if user_obj:
                    username = user_obj.username
            else:
                # cookie validation failed!  redirect to logon page!
                self.redirect(URL_SIGNUP)
                
            
        self.render('signup_confirm_page.html', username=username)
        