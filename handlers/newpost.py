from handler import Handler
from google.appengine.ext import db
from dbmodel import BlogPost, User

class NewPost(Handler):
    """ new blog post class """

    def get(self):
        """ render new blog post form """
        user_d = self.request.cookies.get('user_id')
        if user_d:
            details = {"logout": "Logout"}
            self.render("new.html", **details)
        else:
            self.redirect("/login")

    def post(self):
        """ create new blog post """
        subject = self.request.get("subject")
        post = self.request.get("post")
        user_d = self.request.cookies.get('user_id').split("|")[0]
        if user_d:
            if subject and post:
                user = User.get_by_id(int(user_d))
                new_post = BlogPost(
                    subject=subject, content=post, created_by=user_d, username=user.username)
                new_post.put()
                new_post_id = new_post.key().id()
                self.redirect("/single?post_id=" + str(new_post_id))
            else:
                details = {"error": "you need both subject and content"}
                self.render("new.html", **details)
        else:
            self.redirect("/login")
            