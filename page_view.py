from urls import *
from pagebase import BaseApp, BaseHandler, cleanpath
from model_wikientry import WikiPosts
from model_user import Users

class ViewHandler(BaseHandler):
    @cleanpath
    def get(self, path):
        LINKS_IN = (('edit', '/_edit' + path),
                    ('history', '/_history' + path),
                    ('logout', '/logout' + path))
        LINKS_OUT = (('history', '/_history' + path),
                     ('log in', '/login'),
                     ('sign up', '/signup'))
        
        vdata = dict(self.request.params)
        vdata['user'] = self.user
        vdata['path'] = path
        vdata['linkinfo'] = LINKS_IN if self.user else LINKS_OUT
        
        post_id = vdata.get('v')
        if post_id:
            post_rec = WikiPosts.by_id(path, post_id)
        else:
            post_rec = WikiPosts.most_recent_by_path(path)

        if post_rec:
            vdata['post'] = post_rec
            user_rec = Users.by_id(post_rec.user_id)
            vdata['username'] = user_rec.username
            
            self.render('wikiview.html', vdata=vdata)
        else:
            # We couldn't find a post record.  What we do now
            # depends on the type of item we're trying to view.
            # if it's a DB reference, we're stuck so show an error.
            # If it's a path, we switch to edit mode.
            if post_id:
                self.error(404)
            else:
                # if user not logged in, edit page handler will redirect to login.
                # Do we want to have a double redirect???
                url = URL_RD_EDIT.format(path)
                self.redirect(url)
