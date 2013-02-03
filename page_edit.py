from urls import *
from pagebase import BaseApp, BaseHandler, cleanpath
from model_wikientry import WikiPosts

class EditHandler(BaseHandler):
    @cleanpath
    def get(self, path):
        if not self.user:
            # no logged in user, this is not allowed.  redirect to login page.
            self.redirect(URL_LOGIN)

        LINKS_IN = (('view', path),
                    ('history', '/_history' + path),
                    ('logout', '/logout' + path))
        
        vdata = dict(self.request.params)
        vdata['user'] = self.user
        vdata['path'] = path
        vdata['linkinfo'] = LINKS_IN
        
        post_rec = WikiPosts.most_recent_by_path(path)
        if post_rec:
            vdata['content'] = post_rec.content
        self.render("wikiedit.html", vdata=vdata)
     
    @cleanpath  
    def post(self, path):
        if not self.user:
            self.redirect(URL_LOGIN)
            
        vdata = dict(self.request.params)
        content = self.request.get('content')
        if not content:
            vdata['e_entry'] = "Please enter some text"
            post_rec = WikiPosts.most_recent_by_path(path)
            if post_rec:
                vdata['content'] = post_rec.content
            self.render("wikiedit.html", vdata=vdata)
        else:
            new_rec = WikiPosts.register(path, content, self.user.key().id())
            new_rec.put()
            
#            host_url = self.request.host_url
#            full_url = host_url + path
#            self.response.headers.add_header('Location', full_url)
#            self.response.set_status(302)
            self.redirect(path, permanent=False)