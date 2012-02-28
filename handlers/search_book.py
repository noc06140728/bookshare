# coding: utf-8
import string
from handlers.base import BaseHandler

from entities.usersbook import UsersBook
import basic_auth
from exception import AppError

class SearchBookPage(BaseHandler):
    @basic_auth.required()
    def get(self):
        self.render_template('search_book.html')

    @basic_auth.required()
    def post(self):
        try:
            keyword = self.request.get('q')
            if not string.strip(keyword):
                raise AppError(u'キーワードが入力されていません。')

            books = UsersBook.search(keyword)
            self.render_template('search_book.html', {'keyword': keyword, 'books': books})
        except AppError, e:
            self.render_template('search_book.html', {'error_msg': e.message})

