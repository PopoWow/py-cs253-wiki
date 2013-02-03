from urls import *
from pagebase import BaseApp, BaseHandler, cleanpath
from model_wikientry import WikiPosts
from model_user import Users

class HistoryHandler(BaseHandler):
    @cleanpath
    def get(self, path):
        LINKS_IN = (('edit', '/_edit' + path),
                    ('logout', '/logout' + path))
        LINKS_OUT = (('log in', '/login'),
                     ('sign up', '/signup'))

        vdata = dict(self.request.params)
        vdata['path'] = path
        vdata['user'] = self.user
        vdata['linkinfo'] = LINKS_IN if self.user else LINKS_OUT
        
        vdata['queryresults'] = WikiPosts.by_path(path)
        vdata['usernames'] = {}

        for rec in vdata['queryresults']:
            if not vdata['usernames'].get(rec.user_id):
                user = Users.by_id(rec.user_id)
                vdata['usernames'][rec.user_id] = user.username
        
        self.render("historyview.html", vdata=vdata)
        