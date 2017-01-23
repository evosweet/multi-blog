from handler import Handler

class Logout(Handler):
    """ logout handler"""
    def get(self):
        """ Delete user cookie """
        self.response.delete_cookie('user_id')
        self.redirect("/login")
        