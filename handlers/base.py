import webapp2
import jinja2
import os

jinja_environment = jinja2.Environment(autoescape=True,
        loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../templates')))

class BaseHandler(webapp2.RequestHandler):

    def render_template(self, name, attr=None):
        template = jinja_environment.get_template(name)
        if attr:
            self.response.out.write(template.render(attr))
        else:
            self.response.out.write(template.render())