import base64
import hashlib

from entities.user import User

class BasicAuthError(Exception):
    pass

def required(realm=None):
    def decorator(func):
        def handler(self, *args, **kw):
            try:
                (method, encoded) = self.request.headers['AUTHORIZATION'].split()
                if method.lower() == 'basic':
                    (login_id, password) = base64.b64decode(encoded).split(':')
                    user = User.get_by_key_name(login_id)
                    if not user:
                        raise BasicAuthError
                    if user.password == hashlib.md5(login_id + password).hexdigest():
                        globals()['get_current_user'] = lambda : user
                        return func(self, *args, **kw)
                    raise BasicAuthError
            except (KeyError, BasicAuthError), e:
                self.response.set_status(401)
                self.response.headers['WWW-Authenticate'] = 'Basic realm="%s"' % (realm or 'Default')
                self.response.write(e)
                return
        return handler
    return decorator

def get_current_user():
    pass
