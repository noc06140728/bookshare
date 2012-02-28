from handlers.base import BaseHandler

class HomePage(BaseHandler):
    def get(self):
        self.render_template('home.html')

