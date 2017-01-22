import re, random, string
from handler import Handler
from google.appengine.ext import db

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


class Singup(Handler):
    """ Singup up processing class """

    def val_pass(self, password, verify):
        """ check and verify password """
        if PASS_RE.match(password):
            if password == verify:
                return True, password
            else:
                return False, "Passwords Don't Match"
        else:
            return False, "Invalid Password"

    def val_username(self, username):
        """ username validation"""
        if USER_RE.match(username):
            return True, username
        else:
            return False, "Invalid Username"

    def val_email(self, email):
        """ validate email address """
        if email <> "":
            if EMAIL_RE.match(email):
                return True, email
            return False, "Invalid Email"
        else:
            return True, "No Email"

    def is_user(self, username):
        """ checks if username exist"""
        row = db.GqlQuery("select * from User where username = :1", username)
        if row.fetch(limit=1) == []:
            return True
        else:
            return False

    def get(self):
        """ render Signup page"""
        signup = {'title': "Subscribe to my Blogs",
                  "username": self.request.get("username")}
        self.render("signup.html", **signup)

    def post(self):
        """ validate and create user"""
        user_val, user = self.val_username(self.request.get("username"))
        pass_val, password = self.val_pass(
            self.request.get("password"), self.request.get("verify"))
        email = self.request.get("email")
        is_user = self.is_user(user)
        # ramdon generated secret
        secret = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(8))
        if email is not None or email <> "":
            email_val, email = self.val_email(email)
        else:
            email_val = True
        if user_val and pass_val and email_val and is_user:
            hash_pass = self.hash_str(password, secret)
            user = User(username=user, password=hash_pass,
                        secret=secret, email=email)
            user.put()
            user_id = user.key().id()
            self.response.headers.add_header(
                'Set-Cookie', 'user_id=%s|%s; Path=/' % (user_id, hash_pass))
            self.redirect("/welcome")
        else:
            userinv = ""
            passinv = ""
            emailinv = ""
            if user_val == False:
                userinv = "Invalid Username"
            if pass_val == False:
                passinv = "Invalid Password"
            if email_val == False:
                emailinv = "Invalid Email"
            if is_user == False:
                userinv = "User Already exist"
            error_dic = {"useinv": userinv, "passinv": passinv,
                         "emailinv": emailinv, "username": user_val, "email": email}
            self.render("signup.html", **error_dic)
