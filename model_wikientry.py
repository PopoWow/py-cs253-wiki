from google.appengine.ext import db
from pagebase import render_str
import numbers

class WikiPosts(db.Model):
    path = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    user_id = db.IntegerProperty(required = True)
    dt_created = db.DateTimeProperty(auto_now_add = True)
    
    @staticmethod
    def wikiposts_key(group = 'default'):
        return db.Key.from_path('wikiposts', group)
    
    @classmethod
    def most_recent_by_path(cls, path):
        return cls.by_path(path).get()
    
    @classmethod
    def by_path(cls, path):
        return cls.all().filter('path =', path).order('-dt_created')
    
    @classmethod
    def by_id(cls, path, post_id):
        try:
            if not isinstance(post_id, numbers.Integral):
                post_id = int(post_id) 
        except:
            post_id = None
        
        if post_id:
            post_rec = WikiPosts.get_by_id(post_id, cls.wikiposts_key())
            if post_rec:
                if post_rec.path == path:
                    return post_rec
            
    @classmethod
    def register(cls, path, content, user_id):
        new_post_rec = cls(parent=cls.wikiposts_key(),
                           path=path,
                           content=content,
                           user_id=user_id)
        return new_post_rec
    
    def render(self, truncate=False, username=None):
        if truncate:
            self._content_formatted = self.content[:100]
        else:
            self._content_formatted = self.content.replace('\n', "<br>")
        return render_str("post.html", user=self, truncate=truncate, username=username)
