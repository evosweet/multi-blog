import webapp2
import hmac
import time
import os
import jinja2

# load template path folder
template_dir = os.path.join(os.path.dirname(__file__), '../temp')
# load templateing engine
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

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
        