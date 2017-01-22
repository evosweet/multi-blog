from handler import Handler
from google.appengine.ext import db
from dbmodel import User, Plikes


class MainPage(Handler):
    """ Application Landing Page """

    def last_20(self):
        """ get the last 20 blog post"""
        records = db.GqlQuery(
            "select * from BlogPost order by created desc limit 20")
        return records.fetch(limit=20)

    def like_count(self, blog_id):
        """ get count of likes by blog id"""
        likes = Plikes.all()
        count = likes.filter("blog_id =", str(blog_id)).count()
        return count

    def get(self):
        """ render the main application landing page """
        user_d = self.request.cookies.get('user_id')
        total_count = {}
        if user_d:
            user_id = user_d.split("|")[0]
            user = User.get_by_id(int(user_id))
            for blod in self.last_20():
                post_id = blod.key().id_or_name()
                total_count[post_id] = self.like_count(post_id)
            index_dic = {'title': "Rayons Blog", 'logout': 'Logout', 'blogs': self.last_20(
            ), 'like_count': total_count, 'username': str(user.username).upper()}
        else:
            index_dic = {'title': "Rayons Blog"}
        self.render("index.html", **index_dic)
        