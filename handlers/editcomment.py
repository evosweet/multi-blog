import time
from handler import Handler
from google.appengine.ext import db
from dbmodel import Bcomments

class EditComment(Handler):
    """ edit comment """

    def get(self):
        """ process / valida edit comment request"""
        user_d = self.request.cookies.get('user_id').split("|")[0]
        com_id = self.request.get("com_id")
        if user_d:
            comment = Bcomments.get_by_id(int(com_id))
            if comment.created_by == user_d:
                context = {"logout": 'Logout', 'comment': comment}
                self.render('/edit_comment.html', **context)
            else:
                self.redirect(
                    "/error?error=you cannot edit this comment")
        else:
            self.redirect("/login")

    def post(self):
        """ process comment update request """
        user_d = self.request.cookies.get('user_id').split("|")[0]
        com = self.request.get('com')
        print com
        com_id = self.request.get('com_id')
        if user_d:
            comment = Bcomments.get_by_id(int(com_id))
            if comment.created_by == user_d:
                comment.comment = com
                comment.put()
                time.sleep(0.2)
                self.redirect("/single?post_id=" + str(comment.blog_id))
            else:
                self.redirect(
                    "/error?error=you cannot edit this comment")
        else:
            self.redirect("/login")
            