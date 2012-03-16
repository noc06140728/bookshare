import urllib
import urllib2
import json
import string

GOOGLE_BOOKS_URI = 'https://www.googleapis.com/books/v1'

def search(Book, keyword):
    data = urllib.urlencode({'q': keyword.encode('utf-8'), 'langRestrict': 'ja', 'maxResults': 40, 'prettyPrint=': False, 'fields': 'items(id,volumeInfo(title,authors,publisher,industryIdentifiers,imageLinks))'})
    res = urllib2.urlopen(GOOGLE_BOOKS_URI + '/volumes?%s' % data)
    root = json.load(res)
    if root.has_key('items'):
        return [__get_book(Book, item) for item in root['items']]
    else:
        return []

def get(Book, volume_id):
    data = urllib.urlencode({'langRestrict': 'ja', 'maxResults': 40, 'prettyPrint=': False, 'fields': 'id,volumeInfo(title,authors,publisher,industryIdentifiers,imageLinks)'})
    try:
        res = urllib2.urlopen(GOOGLE_BOOKS_URI + '/volumes/%s?%s' % (volume_id, data))
        book = __get_book(Book, json.load(res))
    except urllib2.HTTPError:
        book = None
    return book

def get_id_set(keyword):
    data = urllib.urlencode({'q': keyword.encode('utf-8'), 'langRestrict': 'ja', 'maxResults': 40, 'prettyPrint=': False, 'fields': 'items(id)'})
    res = urllib2.urlopen(GOOGLE_BOOKS_URI + '/volumes?%s' % data)
    root = json.load(res)
    if root.has_key('items'):
        return set([ item['id'] for item in root['items'] ])
    else:
        return set([])

def __get_book(Book, item):
    if not item:
        return None

    volume = item['volumeInfo']
    book = Book(key_name=item['id'])
    book.book_id = item['id']
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
    

