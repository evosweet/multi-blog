import webapp2

#import handlers
from handlers import (Signup, Welcome, Login,
                      Logout, NewPost, SinglePost, Edit,
                      Delete, Likes, Comment, EditComment,
                      DeleteComment, MainPage, ErrorHandler)

app = webapp2.WSGIApplication([
    ('/', MainPage), ('/signup', Signup), ('/welcome', Welcome),
    ('/login', Login), ('/logout', Logout), ('/new', NewPost),
    ('/single', SinglePost), ('/edit', Edit), ('/delete', Delete),
    ('/like', Likes), ('/error', ErrorHandler), ('/comment', Comment),
    ('/edit_comment', EditComment), ('/del_com', DeleteComment)
], debug=True)
