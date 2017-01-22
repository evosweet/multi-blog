from google.appengine.ext import db

class Bcomments(db.Model):
    """ Blog comment model """
    comment = db.TextProperty(required=True)
    created_by = db.StringProperty(required=True)
    blog_id = db.StringProperty(required=True)
    username = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    