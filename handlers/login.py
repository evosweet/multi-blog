from handler import Handler
from google.appengine.ext import db

class Login(Handler):
    """ application login """

    def get(self):
        """ render login page """
        self.render("login.html")

    def post(self):
        """ process user login request """
        user = self.request.get("username")
        password = self.request.get("password")
        error = ""
        u_query = db.GqlQuery("select * from User where username = :1", user)
        user_d = u_query.fetch(limit=1)
        if user_d <> []:
            secret = str(user_d[0].secret)
            pass_hash = self.hash_str(password, secret)  # create hash
            if user_d[0].password == pass_hash:  # validate hashed password
                user_id = user_d[0].key().id()
                self.response.headers.add_header(
                    'Set-Cookie', 'user_id=%s|%s; Path=/ ' % (user_id, pass_hash))
                self.redirect("/")
            else:
                error = "Invalid Password"
                self.render("login.html", **{"username": user, "error": error})
        else:
            error = "no such user !!"
            self.render("login.html", **{"username": user, "error": error})
            