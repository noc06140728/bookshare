# coding: UTF-8
import webapp2

from handlers.signup import SignupPage
from handlers.home import HomePage
from handlers.add_book import AddBookPage
from handlers.list_book import ListBookPage
from handlers.delete_book import DeleteBookPage
from handlers.show_book import ShowBookPage
from handlers.search_book import SearchBookPage

app = webapp2.WSGIApplication([
        ('/signup', SignupPage),
        ('/', HomePage),
        ('/add_book', AddBookPage),
        ('/list_book', ListBookPage),
        ('/delete_book', DeleteBookPage),
        ('/show_book', ShowBookPage),
        ('/search_book', SearchBookPage)
    ], debug=True)

