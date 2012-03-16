from google.appengine.ext import db
import amazon_book
book_source = amazon_book

class Book(db.Model):
    book_id = db.StringProperty()
    isbn = db.StringProperty()
    title = db.StringProperty()
    author = db.StringProperty()
    publisher = db.StringProperty()
    image_url = db.LinkProperty()
    
    @classmethod
    def get_by_key_name(cls, book_id, parent=None):
        book = super(Book, cls).get_by_key_name(book_id)
        if not book:
            book = book_source.get(cls, book_id)
            if book:
                book.put()
        return book
    
    @classmethod
    def search(cls, keyword):
        return book_source.search(cls, keyword)
    
    @classmethod
    def get_id_set(cls, keyword):
        return book_source.get_id_set(keyword)

