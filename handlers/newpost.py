from handler import Handler
from google.appengine.ext import db
from dbmodel import BlogPost, User
from modelcheck import user_logged_in

class NewPost(Handler):
    """ new blog post class """

    @user_logged_in
    def get(self):
        """ render new blog post form """
        details = {"logout": "Logout"}
        self.render("new.html", **details)

    @user_logged_in
    def post(self):
        """ create new blog post """
        subject = self.request.get("subject")
        post = self.request.get("post")
        user_d = self.request.cookies.get('user_id').split("|")[0]
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
