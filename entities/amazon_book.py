import bottlenose
import lxml.etree
import config

ns={'a': 'http://webservices.amazon.com/AWSECommerceService/2011-08-01'}

amazon = bottlenose.Amazon(config.AWS_ACCESS_KEY_ID, config.AWS_SECRET_ACCESS_KEY, config.ASSOCIATE_TAG, Region='JP')

def search(Book, keyword):
    resp = amazon.ItemSearch(Keywords=keyword, ResponseGroup='ItemAttributes,Images', SearchIndex='Books')
    root = lxml.etree.fromstring(resp)
    items = root.xpath('//a:Item', namespaces=ns)
    return [__get_book(Book, item) for item in items]

def get(Book, asin):
    resp = amazon.ItemLookup(ItemId=asin, ResponseGroup='ItemAttributes,Images')
    root = lxml.etree.fromstring(resp)
    items = root.xpath('//a:Item', namespaces=ns)
    if len(items) > 0:
        return __get_book(Book, items[0])
    else:
        return None

def get_id_set(keyword):
    resp = amazon.ItemSearch(Keywords=keyword, SearchIndex='Books')
    root = lxml.etree.fromstring(resp)
    items = root.xpath('//a:Item', namespaces=ns)
    return set([item.find('a:ASIN', namespaces=ns).text for item in items])

def __get_book(Book, item):
    if not item:
        return None

    asin = item.find('a:ASIN', namespaces=ns).text
    book = Book(key_name=asin)
    book.book_id = asin

    isbn = item.find('a:ItemAttributes/a:ISBN', namespaces=ns)
    book.isbn = isbn.text if isbn <> None else None

    book.title = item.find('a:ItemAttributes/a:Title', namespaces=ns).text

    author = item.find('a:ItemAttributes/a:Author', namespaces=ns)
    book.author = author.text if author <> None else None

    publisher = item.find('a:ItemAttributes/a:Publisher', namespaces=ns)
    book.publisher = publisher.text if publisher <> None else None

    image_url = item.find('a:MediumImage/a:URL', namespaces=ns)
    book.image_url = image_url.text if image_url <> None else None

    return book

