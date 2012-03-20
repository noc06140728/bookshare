# coding: utf-8
from google.appengine.api import mail
from exception import AppError
import sysconf

def get_tenant_id(email):
    email_part = email.split('@')

    if not mail.is_email_valid(email):
        raise (u'正しくないメールアドレスです。')

    if not email_part[1] in sysconf.ALLOWED_DOMAINS.keys():
        raise AppError(u'認められていないメールアドレスです。')

    return sysconf.ALLOWED_DOMAINS[email_part[1]]

