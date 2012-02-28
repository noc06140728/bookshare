# coding: utf-8
from handlers.base import BaseHandler

from entities.book import Book
from entities.usersbook import UsersBook
import basic_auth
from exception import AppError

class ShowBookPage(BaseHandler):
    @basic_auth.required()
    def get(self):
        volume_id = self.request.get('id')
        try:
            book = Book.get_by_key_name(volume_id)
            if not book:
                raise AppError(u'指定された本は見つかりませんでした。')
            users = UsersBook.get_by_volume_id(volume_id)
            self.render_template('show_book.html', {'book': book, 'users': users})
        except AppError, e:
            self.render_template('error.html', {'error_msg': e.message})

