from handler import Handler
from google.appengine.ext import db
from dbmodel import BlogPost


class Delete(Handler):
    """ delete records """

    def get(self):
        """ delete blog post """
        user_d = self.request.cookies.get('user_id')
        post_id = self.request.get("post_id")
        blogpost = BlogPost.get_by_id(int(post_id))
        if user_d:
            if blogpost.created_by == user_d.split("|")[0]:
                blogpost.delete()
                self.redirect("/welcome")
            else:
                self.redirect("/login")
        else:
            self.redirect("/login")
            