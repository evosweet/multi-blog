from handler import Handler
from modelcheck  import user_logged_in
class ErrorHandler(Handler):
    """ general error processing """

    @user_logged_in
    def get(self):
        """ process errors"""
        error = self.request.get("error")
        context = {'error': error, "logout": 'Logout'}
        self.render("/error.html", **context)
