import os
import webapp2
import jinja2
import random
import string
import time
import re
import hmac
from google.appengine.ext import db

#import db models
from dbmodel.user import User
from dbmodel.plikes import Plikes
from dbmodel.blogpost import BlogPost
from dbmodel.bcomment import Bcomments

#import handlers
from handlers import Singup, Welcome, Login, Logout, NewPost

# load template path folder
template_dir = os.path.join(os.path.dirname(__file__), 'temp')
# load templateing engine
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

# Global regrex
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


class Handler(webapp2.RequestHandler):
    """ general template render functions """

    def hash_str(self, in_string, secret):
        """ generate slated hash"""
        return hmac.new(secret, in_string).hexdigest()

    def render_str(self, template, **params):
        """ helper render method"""
        temp = jinja_env.get_template(template)
        return temp.render(params)

    def write(self, *a, **kw):
        """ generic responce"""
        self.response.out.write(*a, **kw)

    def render(self, template, **kw):
        """ generic template render"""
        self.write(self.render_str(template, **kw))


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


# class Signup(Handler):
#     """ sing up processing class """

#     def val_pass(self, password, verify):
#         """ check and verify password """
#         if PASS_RE.match(password):
#             if password == verify:
#                 return True, password
#             else:
#                 return False, "Passwords Don't Match"
#         else:
#             return False, "Invalid Password"

#     def val_username(self, username):
#         """ username validation"""
#         if USER_RE.match(username):
#             return True, username
#         else:
#             return False, "Invalid Username"

#     def val_email(self, email):
#         """ validate email address """
#         if email <> "":
#             if EMAIL_RE.match(email):
#                 return True, email
#             return False, "Invalid Email"
#         else:
#             return True, "No Email"

#     def is_user(self, username):
#         """ checks if username exist"""
#         row = db.GqlQuery("select * from User where username = :1", username)
#         if row.fetch(limit=1) == []:
#             return True
#         else:
#             return False

#     def get(self):
#         """ render Signup page"""
#         signup = {'title': "Subscribe to my Blogs",
#                   "username": self.request.get("username")}
#         self.render("signup.html", **signup)

#     def post(self):
#         """ validate and create user"""
#         user_val, user = self.val_username(self.request.get("username"))
#         pass_val, password = self.val_pass(
#             self.request.get("password"), self.request.get("verify"))
#         email = self.request.get("email")
#         is_user = self.is_user(user)
#         # ramdon generated secret
#         secret = ''.join(random.choice(
#             string.ascii_uppercase + string.digits) for _ in range(8))
#         if email is not None or email <> "":
#             email_val, email = self.val_email(email)
#         else:
#             email_val = True
#         if user_val and pass_val and email_val and is_user:
#             hash_pass = self.hash_str(password, secret)
#             user = User(username=user, password=hash_pass,
#                         secret=secret, email=email)
#             user.put()
#             user_id = user.key().id()
#             self.response.headers.add_header(
#                 'Set-Cookie', 'user_id=%s|%s; Path=/' % (user_id, hash_pass))
#             self.redirect("/welcome")
#         else:
#             userinv = ""
#             passinv = ""
#             emailinv = ""
#             if user_val == False:
#                 userinv = "Invalid Username"
#             if pass_val == False:
#                 passinv = "Invalid Password"
#             if email_val == False:
#                 emailinv = "Invalid Email"
#             if is_user == False:
#                 userinv = "User Already exist"
#             error_dic = {"useinv": userinv, "passinv": passinv,
#                          "emailinv": emailinv, "username": user_val, "email": email}
#             self.render("signup.html", **error_dic)


# class Welcome(Handler):
#     """ main user landing page after login """

#     def post_by_user(self, created_by):
#         """ get post by user """
#         records = db.GqlQuery(
#             "select * from BlogPost where created_by = :1 order by created desc", created_by)
#         return records.fetch(limit=10)

#     def get(self):
#         """ render single user post"""
#         time.sleep(1)  # added sleep to allow db to update
#         user_d = self.request.cookies.get('user_id')
#         if user_d:
#             user_id, user_hash = user_d.split("|")
#             user = User.get_by_id(int(user_id))
#             if user:
#                 if user.password == user_hash:
#                     blog_post = self.post_by_user(user_id)
#                     details = {"username": str(user.username).upper(
#                     ), "logout": "Logout", "blog_post": blog_post}
#                     self.render("welcome.html", **details)
#                 else:
#                     self.redirect("/signup")
#             else:
#                 self.redirect("/signup")
#         else:
#             self.redirect("/signup")


# class Login(Handler):
#     """ application login """

#     def get(self):
#         """ render login page """
#         self.render("login.html")

#     def post(self):
#         """ process user login request """
#         user = self.request.get("username")
#         password = self.request.get("password")
#         error = ""
#         u_query = db.GqlQuery("select * from User where username = :1", user)
#         user_d = u_query.fetch(limit=1)
#         if user_d <> []:
#             secret = str(user_d[0].secret)
#             pass_hash = self.hash_str(password, secret)  # create hash
#             if user_d[0].password == pass_hash:  # validate hashed password
#                 user_id = user_d[0].key().id()
#                 self.response.headers.add_header(
#                     'Set-Cookie', 'user_id=%s|%s; Path=/ ' % (user_id, pass_hash))
#                 self.redirect("/")
#             else:
#                 error = "Invalid Password"
#                 self.render("login.html", **{"username": user, "error": error})
#         else:
#             error = "no such user !!"
#             self.render("login.html", **{"username": user, "error": error})


# class Logout(Handler):

#     def get(self):
#         """ Delete user cookie """
#         self.response.delete_cookie('user_id')
#         self.redirect("/login")


# class NewPost(Handler):
#     """ new blog post class """

#     def get(self):
#         """ render new blog post form """
#         user_d = self.request.cookies.get('user_id')
#         if user_d:
#             details = {"logout": "Logout"}
#             self.render("new.html", **details)
#         else:
#             self.redirect("/login")

#     def post(self):
#         """ create new blog post """
#         subject = self.request.get("subject")
#         post = self.request.get("post")
#         user_d = self.request.cookies.get('user_id').split("|")[0]
#         if user_d:
#             if subject and post:
#                 user = User.get_by_id(int(user_d))
#                 new_post = BlogPost(
#                     subject=subject, content=post, created_by=user_d, username=user.username)
#                 new_post.put()
#                 new_post_id = new_post.key().id()
#                 self.redirect("/single?post_id=" + str(new_post_id))
#             else:
#                 details = {"error": "you need both subject and content"}
#                 self.render("new.html", **details)
#         else:
#             self.redirect("/login")


class SinglePost(Handler):
    """ display single post"""

    def get_comments(self, blog_id):
        """ get comments for a single post """
        records = db.GqlQuery(
            "select * from Bcomments where blog_id = :1", blog_id)
        return records.fetch(limit=100)

    def get(self):
        """ render single blog post """
        post_id = self.request.get("post_id")
        blogpost = BlogPost.get_by_id(int(post_id))
        if blogpost:
            comments = self.get_comments(post_id)
            details = {"blogpost": blogpost, "logout": 'Logout',
                       'post_id': post_id, 'comments': comments}
            self.render("/single.html", **details)
        else:
            self.redirect('/')


class Edit(Handler):
    """ Edit Post """

    def get(self):
        """ edit post"""
        post_id = self.request.get("post_id")
        user_d = self.request.cookies.get('user_id')
        if user_d:
            blogpost = BlogPost.get_by_id(int(post_id))
            if blogpost.created_by == user_d.split("|")[0]:
                details = {"blogpost": blogpost,
                           "logout": 'Logout', 'post_id': post_id}
                self.render("/edit.html", **details)
            else:
                self.redirect("/error?error=You cannot edit this post")
        else:
            self.redirect("/login")

    def post(self):
        """ supdate blog post """
        user_d = self.request.cookies.get('user_id')
        post_id = self.request.get("post_id")
        subject = self.request.get("subject")
        post = self.request.get("post")
        if user_d:
            blogpost = BlogPost.get_by_id(int(post_id))
            if blogpost.created_by == user_d.split("|")[0]:
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
            else:
                self.redirect("/login")


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


class Comment(Handler):
    """ add comment """

    def get(self):
        """ process / validate comment request """
        user_d = self.request.cookies.get('user_id')
        post_id = self.request.get("post_id")
        blogpost = BlogPost.get_by_id(int(post_id))
        if user_d:
            context = {"logout": 'Logout', 'post_id': post_id}
            self.render("/comment.html", **context)
        else:
            self.redirect("/login")

    def post(self):
        """ create / validate comment """
        user_d = self.request.cookies.get('user_id').split("|")[0]
        post_id = self.request.get("post_id")
        comment = self.request.get("comment")
        if user_d:
            if comment:
                user = User.get_by_id(int(user_d))
                comment = Bcomments(
                    comment=comment, created_by=user_d, blog_id=post_id, username=user.username)
                comment.put()
                time.sleep(0.2)
                self.redirect("/single?post_id=" + post_id)
            else:
                context = {
                    'error': 'you need to submit a comment !!!', "logout": 'Logout'}
                self.render("/comment.html", **context)
        else:
            self.redirect("/login")


class EditComment(Handler):
    """ edit comment """

    def get(self):
        """ process / valida edit comment request"""
        user_d = self.request.cookies.get('user_id').split("|")[0]
        com_id = self.request.get("com_id")
        if user_d:
            comment = Bcomments.get_by_id(int(com_id))
            if comment.created_by == user_d:
                context = {"logout": 'Logout', 'comment': comment}
                self.render('/edit_comment.html', **context)
            else:
                self.redirect(
                    "/error?error=you cannot edit this comment")
        else:
            self.redirect("/login")

    def post(self):
        """ process comment update request """
        user_d = self.request.cookies.get('user_id').split("|")[0]
        com = self.request.get('com')
        print com
        com_id = self.request.get('com_id')
        if user_d:
            comment = Bcomments.get_by_id(int(com_id))
            if comment.created_by == user_d:
                comment.comment = com
                comment.put()
                time.sleep(0.2)
                self.redirect("/single?post_id=" + str(comment.blog_id))
            else:
                self.redirect(
                    "/error?error=you cannot edit this comment")
        else:
            self.redirect("/login")


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


class ErrorHandler(Handler):
    """ general error processing """

    def get(self):
        """ process errors"""
        user_d = self.request.cookies.get('user_id')
        error = self.request.get("error")
        if user_d:
            context = {'error': error, "logout": 'Logout'}
        else:
            context = {'error': error}
        self.render("/error.html", **context)


app = webapp2.WSGIApplication([
    ('/', MainPage), ('/signup', Singup), ('/welcome', Welcome),
    ('/login', Login), ('/logout', Logout), ('/new', NewPost),
    ('/single', SinglePost), ('/edit', Edit), ('/delete', Delete),
    ('/like', Likes), ('/error', ErrorHandler), ('/comment', Comment),
    ('/edit_comment', EditComment), ('/del_com', DeleteComment)
], debug=True)
