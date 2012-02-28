from google.appengine.ext import db

class User(db.Model):
    email = db.EmailProperty(required=True)
    password = db.StringProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)

