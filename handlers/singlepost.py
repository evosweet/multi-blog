from google.appengine.ext import db
from handler import Handler
from dbmodel import BlogPost
from modelcheck import user_logged_in, post_exists


class SinglePost(Handler):
    """ display single post"""

    def get_comments(self, blog_id):
        """ get comments for a single post """
        records = db.GqlQuery(
            "select * from Bcomments where blog_id = :1", blog_id)
        return records.fetch(limit=100)

    @user_logged_in
    @post_exists
    def get(self):
        """ render single blog post """
        post_id = self.request.get("post_id")
        blogpost = BlogPost.get_by_id(int(post_id))
        comments = self.get_comments(post_id)
        details = {"blogpost": blogpost, "logout": 'Logout',
                    'post_id': post_id, 'comments': comments}
        self.render("/single.html", **details)
        