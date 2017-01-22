import time
from handler import Handler
from dbmodel import Bcomments

class DeleteComment(Handler):
    """ delete comment"""

    def get(self):
        """ delete comment """
        com_id = self.request.get("com_id")
        post_id = self.request.get("post_id")
        user_id = self.request.get("created_by")
        user_d = self.request.cookies.get('user_id').split("|")[0]
        if user_d:
            if user_d == user_id:
                com = Bcomments.get_by_id(int(com_id))
                com.delete()
                time.sleep(0.2)
                self.redirect("/single?post_id=" + str(post_id))
            else:
                self.redirect(
                    "/error?error=you can only delete your own comment")
        else:
            self.redirect("/login")

