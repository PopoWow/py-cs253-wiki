from urls import *
from pagebase import BaseApp, BaseHandler

class EditHandler(BaseHandler):
    def get(self, id):
        self.response.write('Edit page: detected ID: {}'.format(id))