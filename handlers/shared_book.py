# coding: utf-8
import string
from handlers.base import BaseHandler

from entities.usersbook import UsersBook
import basic_auth
from exception import AppError

class SharedBookPage(BaseHandler):
    @basic_auth.required()
    def get(self):
        try:
            books = UsersBook.all_books()
            self.render_template('shared_book.html', {'books': books})
        except AppError, e:
            self.render_template('shared_book.html', {'error_msg': e.message})

