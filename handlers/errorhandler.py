from handler import Handler

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
