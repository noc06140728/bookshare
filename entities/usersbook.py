from google.appengine.ext import db
from google.appengine.api import memcache
from user import User
from book import Book

class UsersBook(db.Model):
    user = db.ReferenceProperty(User)
    volume_id = db.StringProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def all_books(cls):
        ubook_id_set = cls.__get_book_id_set()
        return [Book.get_by_key_name(volume_id) for volume_id in ubook_id_set]
    
    @classmethod
    def search(cls, keyword):
        ubook_id_set = cls.__get_book_id_set()
        book_id_set = Book.get_id_set(keyword)
        id_list = list(ubook_id_set & book_id_set)[:30]
        return [Book.get_by_key_name(volume_id) for volume_id in id_list]
    
    @classmethod
    def get_by_volume_id(cls, volume_id):
        return UsersBook.gql('WHERE volume_id = :1', volume_id)
    
    @classmethod
    def get_by_user(cls, user):
        return UsersBook.gql('WHERE user = :1', user)
    
    @classmethod
    def __get_book_id_set(cls):
        book_id_set = memcache.get('UsersBook.id_set')
        if not book_id_set:
            ubooks = cls.all()
            book_id_set = set(ubook.volume_id for ubook in ubooks)
            memcache.set('UsersBook.id_set', book_id_set)
        return book_id_set

    def put(self):
        self.__delete_cache()
        super(UsersBook, self).put()

    def delete(self):
        self.__delete_cache()
        super(UsersBook, self).delete()

    def __delete_cache(self):
        memcache.delete('UsersBook.id_set')

