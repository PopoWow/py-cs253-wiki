from urls import *
from pagebase import BaseApp, BaseHandler

class ViewHandler(BaseHandler):
    def get(self, id):
        self.response.write('View  page: detected ID: {}'.format(id))
        
        # if the post does not appear in the database, we redirect to
        # the edit page
