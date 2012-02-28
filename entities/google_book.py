import urllib
import urllib2
import json

GOOGLE_BOOKS_URI = 'https://www.googleapis.com/books/v1'

def search(keyword):
    data = urllib.urlencode({'q': keyword.encode('utf-8'), 'langRestrict': 'ja', 'maxResults': 40, 'prettyPrint=': False, 'fields': 'items(id,volumeInfo(title,authors,publisher,industryIdentifiers,imageLinks))'})
    res = urllib2.urlopen(GOOGLE_BOOKS_URI + '/volumes?%s' % data)
    root = json.load(res)
    books = []
    if root.has_key('items'):
        for item in root['items']:
            books.append(item)
    return books

def get(volume_id):
    data = urllib.urlencode({'langRestrict': 'ja', 'maxResults': 40, 'prettyPrint=': False, 'fields': 'id,volumeInfo(title,authors,publisher,industryIdentifiers,imageLinks)'})
    try:
        res = urllib2.urlopen(GOOGLE_BOOKS_URI + '/volumes/%s?%s' % (volume_id, data))
        root = json.load(res)
    except urllib2.HTTPError:
        root = None
    return root

def get_id_set(keyword):
    data = urllib.urlencode({'q': keyword.encode('utf-8'), 'langRestrict': 'ja', 'maxResults': 40, 'prettyPrint=': False, 'fields': 'items(id)'})
    res = urllib2.urlopen(GOOGLE_BOOKS_URI + '/volumes?%s' % data)
    root = json.load(res)
    if root.has_key('items'):
        return set([ item['id'] for item in root['items'] ])
    else:
        return set([])
