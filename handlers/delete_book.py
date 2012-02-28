# coding: utf-8
from handlers.base import BaseHandler

from entities.usersbook import UsersBook
import basic_auth
from exception import AppError

class DeleteBookPage(BaseHandler):
    @basic_auth.required()
    def get(self):
        try:
            volume_id = self.request.get('id')
            if volume_id:
                user = basic_auth.get_current_user()
                ubook = UsersBook.get_by_key_name(volume_id+':'+user.email)
                if not ubook:
                    raise AppError(u'指定された本の登録はありません。')
                ubook.delete()
            self.redirect('/list_book')
        except AppError, e:
            self.render_template('error.html', {'error_msg': e.message})
            
