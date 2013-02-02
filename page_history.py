from urls import *
from pagebase import BaseApp, BaseHandler

class HistoryHandler(BaseHandler):
    def get(self, id):
        params = self.request.params
        ver = params['v']
        self.response.write('History page: detected ID and URI param: {}'.format(ver))
        