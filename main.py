import os
import webapp2
import jinja2
import random
import string
import time
import re
import hmac
from google.appengine.ext import db

#import db models
from dbmodel.user import User
from dbmodel.plikes import Plikes
from dbmodel.blogpost import BlogPost
from dbmodel.bcomment import Bcomments

#import handlers
from handlers import (Signup, Welcome, Login,
                      Logout, NewPost, SinglePost, Edit,
                      Delete, Likes, Comment, EditComment,
                      DeleteComment, MainPage, ErrorHandler)

# # load template path folder
# template_dir = os.path.join(os.path.dirname(__file__), 'temp')
# # load templateing engine
# jinja_env = jinja2.Environment(
#     loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

# Global regrex
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")



app = webapp2.WSGIApplication([
    ('/', MainPage), ('/signup', Signup), ('/welcome', Welcome),
    ('/login', Login), ('/logout', Logout), ('/new', NewPost),
    ('/single', SinglePost), ('/edit', Edit), ('/delete', Delete),
    ('/like', Likes), ('/error', ErrorHandler), ('/comment', Comment),
    ('/edit_comment', EditComment), ('/del_com', DeleteComment)
], debug=True)
