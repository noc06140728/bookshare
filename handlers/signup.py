# coding: utf-8
import string
import hashlib

from google.appengine.api import namespace_manager
from google.appengine.api import mail

from entities.user import User
from entities.activate_key import ActivateKey
from exception import AppError
from handlers.base import BaseHandler
import tenant

class SignupPage(BaseHandler):
    def get(self):
        self.render_template('signup.html')

    def post(self):
        try:
            email = self.request.get('email')
            hkey = self.request.get('hkey')
            
            tenant_id = tenant.get_tenant_id(email)
            namespace_manager.set_namespace(tenant_id)

            if User.get_by_key_name(email):
                raise AppError(u'このメールアドレスは、既に登録されています。')

            if self.request.get('button') == 'Send Activate Key':
                key = ActivateKey.make(email)
                self.send_activate_key(email, key[:12])
                hkey = key[12:]
                self.render_template('signup.html', {'email': email, 'hkey': hkey})
                return
            else:
                key = self.request.get('key1') + self.request.get('key2') + self.request.get('key3') + self.request.get('hkey')
                if not ActivateKey.validate(email, key):
                    raise AppError(u'不正な Activate Key です。')
                password = self.request.get('password')
                if not string.strip(password):
                    raise AppError(u'パスワードが未入力です。')
                user = User(key_name=email, email=email, password=hashlib.md5(email + password).hexdigest())
                user.put()
                self.redirect('/')

        except AppError, e:
            self.render_template('signup.html', {'error_msg': e.message, 'email': email, 'hkey': hkey})

    def send_activate_key(self, email, key):
        mail.send_mail(sender='Masahiro Namba <mnanba@ryobi-sol.co.jp>',
              to=email,
              subject='Your Activate Key',
              body='Your Activate Key: %s-%s-%s' % (key[0:4], key[4:8], key[8:12]))

