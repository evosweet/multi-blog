import time
from handler import Handler
from google.appengine.ext import db
from dbmodel import Plikes, BlogPost


class Likes(Handler):
    """ likes or unlike post"""

    def count_likes(self, created_by, blog_id):
        """ get a count of likes by id """
        results = db.GqlQuery(
            "select * from Plikes where created_by = :1 and blog_id = :2", created_by, blog_id)
        count = results.fetch(limit=1)
        if count <> []:
            return 0
        else:
            return 1

    def unlike(self, user_id, blog_id):
        """ delete like by id """
        results = db.GqlQuery(
            "select * from Plikes where created_by = :1 and blog_id = :2", user_id, blog_id)
        results.fetch(limit=1)
        if results <> []:
            results[0].delete()
        else:
            pass  # do nothing

    def get(self):
        """ process like unlike request """
        user_d = self.request.cookies.get('user_id').split("|")[0]
        post_id = self.request.get("post_id")
        req_type = self.request.get("type")
        blogpost = BlogPost.get_by_id(int(post_id))
        if user_d:
            if blogpost.created_by == user_d:
                self.redirect("/error?error=You Cannot Like Your Own Post")
            else:
                if req_type == 'unlike':
                    self.unlike(user_d, post_id)
                    time.sleep(0.2)
                    self.redirect("/")
                else:
                    count = self.count_likes(user_d, post_id)
                    if count == 1:
                        likes = Plikes(created_by=user_d, blog_id=post_id)
                        likes.put()
                        time.sleep(0.2)
                        self.redirect("/")
                    else:
                        self.redirect(
                            "/error?error=You Already Liked This Post")
        else:
            self.redirect("/login")
            