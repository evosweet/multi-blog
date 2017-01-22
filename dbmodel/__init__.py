from google.appengine.ext import db


class User(db.Model):
    """ application user model """
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    secret = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    