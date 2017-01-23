import time
from handler import Handler
from google.appengine.ext import db
from dbmodel import User, Bcomments
from modelcheck import user_logged_in

class Comment(Handler):
    """ add comment """

    @user_logged_in
    def get(self):
        """ process / validate comment request """
        post_id = self.request.get("post_id")
        context = {"logout": 'Logout', 'post_id': post_id}
        self.render("/comment.html", **context)

    @user_logged_in
    def post(self):
        """ create / validate comment """
        post_id = self.request.get("post_id")
        comment = self.request.get("comment")
        user_d = self.request.cookies.get('user_id').split('|')[0]
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
