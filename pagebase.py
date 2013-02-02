import os
import webapp2
import jinja2
import jinja_filters
import utils
from model_user import User

# I always like to insert a layer when using 3rd party code like this
# allows for easy injection of my own stuff at a later time.  If you
# plan with this in mind, good things will happen, I feel.

# using the jinja template system here w/ the webapp2 lightweight app
# framework.  jinja renders a template into an html stream.  We take
# that stream and give it to webapp2 to present it to the user.

#initialize jinja
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)
    
class BaseApp(webapp2.WSGIApplication):
    pass

class BaseHandler(webapp2.RequestHandler):
    # jinja helpers.
    # take map of parameters and get jinja to render a template
    def render_str(self, template, **params):
        params['user'] = self.user
        render_str(template, params)

    # user-callable helper to call into jinja and pass result stream to webapp2
    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))

    # write out some stuff via webapp2
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)    
    
    #
    def authenticate_user(self):
        # check the userid cookie and validate the user.
        True
    
    # Cookie support.  Settings a cookie helper
    # Take a value, hash it securely and then set it to be returned to
    # the user in the response.
    def set_secure_cookie(self, name, val):
        cookie_val = utils.create_cookie_hash(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, str(cookie_val)))

    # validate the cookie.  value is rehashed and compared with transmitted
    # hash.  If they equal, cookie was not tampered with.
    # RETURNS: BOOL - Cookie verification result.
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and utils.valid_cookie_hash(cookie_val)

    # user supplied correct password which was checked with DB hash
    # so "login" which just set a user_id cookie.
    def login(self, user_rec):
        self.set_secure_cookie('user_id', str(user_rec.key().id()))

    # clear user_id cookie
    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    # called before each connection.  
    def initialize(self, *a, **kw):
        super(BaseHandler, self).initialize(*a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = User.by_id(int(uid))
