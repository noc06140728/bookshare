from google.appengine.ext import db
import string
import google_book

class Book(db.Model):
    volume_id = db.StringProperty()
    isbn = db.StringProperty()
    title = db.StringProperty()
    author = db.StringProperty()
    publisher = db.StringProperty()
    image_url = db.LinkProperty()
    
    @classmethod
    def get_by_key_name(cls, volume_id, parent=None):
        book = super(Book, cls).get_by_key_name(volume_id)
        if not book:
            book_json = google_book.get(volume_id)
            if book_json:
                book = cls.__get_instance(book_json)
                book.put()
            else:
                book = None
        return book
    
    @classmethod
    def __get_instance(cls, item):
        volume = item['volumeInfo']
        book = Book(key_name=item['id'])
        book.volume_id = item['id']
        if volume.has_key('industryIdentifiers'):
            isbns = [ p['identifier'] for p in volume['industryIdentifiers'] if p['type'] == 'ISBN_10' ]
            if len(isbns) == 1:
                book.isbn = isbns[0]
        if volume.has_key('title'):
            book.title = volume['title']
        if volume.has_key('authors'):
            book.author = string.join(volume['authors'], ', ')
        if volume.has_key('publisher'):
            book.publisher = volume['publisher']
        if volume.has_key('imageLinks'):
            book.image_url = volume['imageLinks']['thumbnail']
        return book
    
    @classmethod
    def search(self, keyword):
        books = google_book.search(keyword)
        return [self.__get_instance(book) for book in books]
    
