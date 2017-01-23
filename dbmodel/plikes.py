from google.appengine.ext import db

class Plikes(db.Model):
    """ Blog like model"""
    blog_id = db.StringProperty(required=True)
    created_by = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
