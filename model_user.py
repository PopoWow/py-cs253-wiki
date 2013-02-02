from google.appengine.ext import db
import utils

class BaseModel(db.Model):
    pass

class User(BaseModel):
    username = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty(required = True)
    
    @classmethod
    def users_key(cls, group = 'default'):
        return db.Key.from_path('users', group)

    @classmethod
    def by_id(cls, uid):
        #user_rec = User.get_by_id(uid, parent = cls.users_key())
        user_rec = User.get_by_id(int(uid)) 
        return user_rec

    @classmethod
    # try using Query class for DB access.  Get returns FIRST result.
    # Nice for this usage but keep in mind.
    def by_username(cls, name):
        u = cls.all().filter('username =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = utils.create_pw_hash(name, pw)
        return cls(parent = cls.users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u