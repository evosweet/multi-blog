import time
from handler import Handler
from dbmodel import User
from google.appengine.ext import db

class Welcome(Handler):
    """ main user landing page after login """

    def post_by_user(self, created_by):
        """ get post by user """
        records = db.GqlQuery(
            "select * from BlogPost where created_by = :1 order by created desc", created_by)
        return records.fetch(limit=10)

    def get(self):
        """ render single user post"""
        time.sleep(1)  # added sleep to allow db to update
        user_d = self.request.cookies.get('user_id')
        if user_d:
            user_id, user_hash = user_d.split("|")
            user = User.get_by_id(int(user_id))
            if user:
                if user.password == user_hash:
                    blog_post = self.post_by_user(user_id)
                    details = {"username": str(user.username).upper(
                    ), "logout": "Logout", "blog_post": blog_post}
                    self.render("welcome.html", **details)
                else:
                    self.redirect("/signup")
            else:
                self.redirect("/signup")
        else:
            self.redirect("/signup")
