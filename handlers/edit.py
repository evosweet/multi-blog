from handler import Handler
from google.appengine.ext import db
from dbmodel import BlogPost
from modelcheck import post_exists, user_logged_in, user_owns_post


class Edit(Handler):
    """ Edit Post """
    @user_logged_in
    @post_exists
    @user_owns_post
    def get(self):
        """ edit post"""
        post_id = self.request.get("post_id")
        user_d = self.request.cookies.get('user_id')
        blogpost = BlogPost.get_by_id(int(post_id))
        if blogpost.created_by == user_d.split("|")[0]:
            details = {"blogpost": blogpost,
                       "logout": 'Logout', 'post_id': post_id}
            self.render("/edit.html", **details)
        else:
            self.redirect("/error?error=You cannot edit this post")

    @user_logged_in
    @post_exists
    @user_owns_post
    def post(self):
        """ supdate blog post """
        post_id = self.request.get("post_id")
        subject = self.request.get("subject")
        post = self.request.get("post")
        blogpost = BlogPost.get_by_id(int(post_id))
        if subject and post:
            blogpost.subject = subject
            blogpost.content = post
            blogpost.put()
            details = {"blogpost": blogpost,
                       "logout": 'Logout', 'post_id': post_id}
            self.render("/single.html", **details)
        else:
            details = {"blogpost": blogpost, "logout": 'Logout',
                       "error": "you need both subject and content"}
            self.render("/edit.html", **details)
