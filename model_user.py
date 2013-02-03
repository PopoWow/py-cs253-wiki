from google.appengine.ext import db
import utils

class BaseModel(db.Model):
    pass

class Users(BaseModel):
    username = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty(required = True)
    
    @staticmethod
    def users_key(group = 'default'):
        return db.Key.from_path('users', group)

    @classmethod
    def by_id(cls, uid):
        user_rec = cls.get_by_id(uid, parent = cls.users_key())
        #user_rec = cls.get_by_id(int(uid)) 
        return user_rec

    @classmethod
    # try using Query class for DB access.  Get returns FIRST result.
    # Nice for this usage but keep in mind.
    def by_username(cls, name):
        u = cls.all().filter('username =', name).get()
        return u

    @classmethod
    def register(cls, username, pw, email = None):
        pw_hash = utils.create_pw_hash(username, pw)
        return cls(parent = cls.users_key(),
                    username = username,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        user_rec = cls.by_username(name)
        if user_rec and utils.valid_pw_hash(name, pw, user_rec.pw_hash):
            return user_rec
