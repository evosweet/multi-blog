from google.appengine.ext import db

class BlogPost(db.Model):
    """ application blog model """
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created_by = db.StringProperty(required=True)
    username = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    