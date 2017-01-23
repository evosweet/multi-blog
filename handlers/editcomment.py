import time
from handler import Handler
from google.appengine.ext import db
from dbmodel import Bcomments
from modelcheck import comment_exists, user_logged_in, user_owns_comment


class EditComment(Handler):
    """ edit comment """
    @user_logged_in
    @user_owns_comment
    @comment_exists
    def get(self):
        """ process / valida edit comment request"""
        com_id = self.request.get("com_id")
        comment = Bcomments.get_by_id(int(com_id))
        context = {"logout": 'Logout', 'comment': comment}
        self.render('/edit_comment.html', **context)

    @user_logged_in
    @user_owns_comment
    @comment_exists
    def post(self):
        """ process comment update request """
        com = self.request.get('com')
        com_id = self.request.get('com_id')
        comment = Bcomments.get_by_id(int(com_id))
        if com:
            comment.comment = com
            comment.put()
            time.sleep(0.2)
            self.redirect("/single?post_id=" + str(comment.blog_id))
        else:
            error = "you must have a comment"
            context = {"logout": 'Logout', 'error': error, 'comment': comment}
            self.render('/edit_comment.html', **context)
