import time
from handler import Handler
from google.appengine.ext import db
from dbmodel import User, Bcomments, BlogPost

class Comment(Handler):
    """ add comment """

    def get(self):
        """ process / validate comment request """
        user_d = self.request.cookies.get('user_id')
        post_id = self.request.get("post_id")
        #blogpost = BlogPost.get_by_id(int(post_id))
        if user_d:
            context = {"logout": 'Logout', 'post_id': post_id}
            self.render("/comment.html", **context)
        else:
            self.redirect("/login")

    def post(self):
        """ create / validate comment """
        user_d = self.request.cookies.get('user_id').split("|")[0]
        post_id = self.request.get("post_id")
        comment = self.request.get("comment")
        if user_d:
            if comment:
                user = User.get_by_id(int(user_d))
                comment = Bcomments(
                    comment=comment, created_by=user_d, blog_id=post_id, username=user.username)
                comment.put()
                time.sleep(0.2)
                self.redirect("/single?post_id=" + post_id)
            else:
                context = {
                    'error': 'you need to submit a comment !!!', "logout": 'Logout'}
                self.render("/comment.html", **context)
        else:
            self.redirect("/login")
