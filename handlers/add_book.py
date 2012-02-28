# coding: utf-8
import string
from handlers.base import BaseHandler

from entities.book import Book
from entities.usersbook import UsersBook
import basic_auth
from exception import AppError

class AddBookPage(BaseHandler):
    @basic_auth.required()
    def get(self):
        try:
            volume_id = self.request.get('id')
            if volume_id:
                user = basic_auth.get_current_user()
                book = Book.get_by_key_name(volume_id)
                if not book:
                    raise AppError(u'指定された本は見つかりませんでした。')
                ubook = UsersBook(key_name=volume_id+':'+user.email, user=user, volume_id=volume_id)
                ubook.put()
                self.redirect('/list_book')
            else:
                self.render_template('add_book.html')
        except AppError, e:
            self.render_template('error.html',  {'error_msg': e.message})

    @basic_auth.required()
    def post(self):
        try:
            keyword = self.request.get('q')
            if not string.strip(keyword):
                raise AppError(u'キーワードが入力されていません。')

            books = Book.search(keyword)
            self.render_template('add_book.html', {'keyword': keyword, 'books': books})
        except AppError, e:
            self.render_template('add_book.html', {'error_msg': e.message})

