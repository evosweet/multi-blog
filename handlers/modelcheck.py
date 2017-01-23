from google.appengine.ext import db
from dbmodel import BlogPost, Bcomments

def comment_exists(func):
    """ comment check"""

    def wrapper(self, *args, **Kwargs):
        """ check if comment exist"""
        post_id = self.request.get("com_id")
        key = db.Key.from_path('Bcomments', int(post_id))
        post = db.get(key)
        if post:
            return func(self, *args, **Kwargs)
        else:
            self.redirect('/error?error=this comment does not exist')
    return wrapper


def post_exists(func):
    """ post check"""

    def wrapper(self, *args, **Kwargs):
        """ check if comment exist"""
        post_id = self.request.get("post_id")
        key = db.Key.from_path('BlogPost', int(post_id))
        post = db.get(key)
        if post:
            return func(self, *args, **Kwargs)
        else:
            self.redirect('/error?error=this post does not exist')
    return wrapper

def user_logged_in(func):
    """ check if user logged in"""

    def wrapper(self, *args, **Kwargs):
        """ check user status"""
        user_d = self.request.cookies.get('user_id')
        if user_d:
            return func(self, *args, **Kwargs)
        else:
            self.redirect("/login")
    return wrapper


def user_owns_post(func):
    """ check if user owns post """

    def wrapper(self, *args, **Kwargs):
        """ owner check """
        user_id = self.request.cookies.get('user_id').split('|')[0]
        post_id = self.request.get("post_id")
        blogpost = BlogPost.get_by_id(int(post_id))
        if blogpost.created_by == user_id:
            return func(self, *args, **Kwargs)
        else:
            self.redirect('/error?error=you cannot edit this post !!!')
    return wrapper



def user_owns_comment(func):
    """ check comment owner """

    def wrapper(self, *args, **Kwargs):
        """ comment check """
        user_id = self.request.cookies.get('user_id').split('|')[0]
        com_id = self.request.get("com_id")
        comment = Bcomments.get_by_id(int(com_id))
        if comment.created_by == user_id:
            return func(self, *args, **Kwargs)
        else:
            self.redirect('/error?error=you cannot edit this comment !!!')
    return wrapper

