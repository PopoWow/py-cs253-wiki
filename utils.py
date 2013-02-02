import random
import string
import hashlib
#import hmac
import numbers
from secret import SECRET
import re

####################################
# Cookie Hashing

def create_cookie_hash(cookie_val):
    if isinstance(cookie_val, numbers.Integral) or (type(cookie_val) is str):
        cookie_val = unicode(cookie_val)
    
    # d'oh!  hmac doesn't take UNICODE inputs.  Not sure if this is intentional
    # (seems like it may be) but this kinda sucks for me.  I guess I'll switch
    # sha256(val + SECRET)
    #digest = hmac.new(cookie_val, SECRET).hexdigest()
    val_to_hash = cookie_val + SECRET
    digest = hashlib.sha256(val_to_hash).hexdigest()
    return u"{}|{}".format(cookie_val, digest)

# cookies will be transmitted in the format:  [val]|[hashdigest]
# 5|3453ae88324382a3828328def8238838423
# Hash the first part (after added secret val) and then compare
# if the hashes match, it hasn't been tampered with
def valid_cookie_hash(cookie_hash):
    if type(cookie_hash) is str:
        cookie_hash = unicode(cookie_hash)
        
    split_val = cookie_hash.split(u'|')
    return split_val[0] if (create_cookie_hash(split_val[0]) == cookie_hash) else None

####################################
# Salt

# Create user hashes but also use a salt seed value.  This is to prevent against
# rainbow-table attacks.  Salt is a x-len random char string to add a other values
# to hash.  Prevents a table from being used for more than one password.
def create_salt(salt_len):
    ascii_salt = "".join([random.choice(string.ascii_letters) for x in range(salt_len)])
    return unicode(ascii_salt)
    
def create_pw_hash(name, pw, salt=None, saltlen=5):
    if not type(name) is unicode:
        name = unicode(name)
    if not type(pw) is unicode:
        pw = unicode(pw)
    
    if not salt:
        salt = create_salt(saltlen)
    val_to_hash = name + pw + salt
    return u"{},{}".format(hashlib.sha256(val_to_hash).hexdigest(), salt)

def valid_pw_hash(name, pw, stored_pw_hash):
    val = stored_pw_hash.split(u',')
    return stored_pw_hash == create_pw_hash(name, pw, val[1])

####################################
# user account helpers
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASSWORD_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)


