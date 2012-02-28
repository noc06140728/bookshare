# coding: utf-8
from google.appengine.ext import db
import hashlib
import datetime
from exception import AppError

class ActivateKey(db.Model):
    email = db.EmailProperty(required=True)
    activate_key = db.StringProperty(required=True)
    limit = db.DateTimeProperty(required=True)
    date = db.DateTimeProperty(auto_now=True)
    
    @classmethod
    def make(cls, email):
        akey = ActivateKey.get_by_key_name(email)
        if akey and akey.limit > datetime.datetime.now(): 
            raise AppError(u'既に Activate Key を発行済みです。')
        
        key = ActivateKey(key_name=email, email=email, activate_key=ActivateKey.make_key(email), limit=datetime.datetime.now() + datetime.timedelta(minutes=5))
        key.put()
        return key.activate_key
    
    @classmethod
    def make_key(cls, email):
        return hashlib.md5(email + str(datetime.datetime.now())).hexdigest()[:16]

    @classmethod
    def validate(cls, email, key):
        akey = ActivateKey.get_by_key_name(email)
        return akey and (akey.limit > datetime.datetime.now()) and (akey.activate_key == key)

