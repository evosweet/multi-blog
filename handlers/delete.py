from handler import Handler
from google.appengine.ext import db
from dbmodel import BlogPost
from modelcheck import user_owns_post, user_logged_in, post_exists


class Delete(Handler):
    """ delete records """
    @user_logged_in
    @post_exists
    @user_owns_post
    def get(self):
        """ delete blog post """
        post_id = self.request.get("post_id")
        blogpost = BlogPost.get_by_id(int(post_id))
        blogpost.delete()
        self.redirect("/welcome")
