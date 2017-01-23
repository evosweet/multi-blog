import time
from handler import Handler
from dbmodel import Bcomments
from modelcheck import user_logged_in, comment_exists, user_owns_comment

class DeleteComment(Handler):
    """ delete comment"""

    @user_logged_in
    @comment_exists
    @user_owns_comment
    def get(self):
        """ delete comment """
        com_id = self.request.get("com_id")
        post_id = self.request.get("post_id")
        com = Bcomments.get_by_id(int(com_id))
        com.delete()
        time.sleep(0.2)
        self.redirect("/single?post_id=" + str(post_id))
        