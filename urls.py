RE_TB = '/?' # append to urls in WSGIApplication construction
             # so public url paths take either w/ or w/o a 
             # trailing backslash
RE_TBE = RE_TB + '$'

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

URL_ROOT    = r'/'
URL_SIGNUP  = r'/signup'
URL_LOGIN   = r'/login'
URL_LOGOUT  = r'/logout'
URL_VIEW    = PAGE_RE
URL_EDIT    = r"/_edit" + PAGE_RE
URL_HIST    = r"/_history" + PAGE_RE
#URL_PERMA   = PAGE_RE
#URL_BLOG_J  = URL_BLOG + RE_TB + ".json"
#URL_PERMA_J = URL_PERMA + RE_TB + ".json"
#URL_FLUSH   = URL_BLOG + r'/flush'