# coding: utf-8
from handlers.base import BaseHandler

from entities.book import Book
from entities.user import User
from entities.usersbook import UsersBook
import basic_auth
from exception import AppError

class ListBookPage(BaseHandler):
    @basic_auth.required()
    def get(self):
        try:
            user = basic_auth.get_current_user()
            email = self.request.get('email')
            if email:
                if user.email == email:
                    self.redirect('/list_book')
                    return
                else:
                    friend = User.get_by_key_name(email)
                    if not friend:
                        raise AppError(u'指定されたメールアドレスに該当するユーザはいません。')
                    ubooks = UsersBook.get_by_user(friend)
            else:
                friend = None
                ubooks = UsersBook.get_by_user(user)
            books = [Book.get_by_key_name(ubook.book_id) for ubook in ubooks]
            self.render_template('list_book.html', {'books': books, 'friend': friend})
        except AppError, e:
            self.render_template('list_book.html', {'error_msg': e.message})

