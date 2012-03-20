from entities.config import Config

# Amazon Web Services
AWS_ACCESS_KEY_ID = str(Config.get_conf('AWS_ACCESS_KEY_ID'))
AWS_SECRET_ACCESS_KEY = str(Config.get_conf('AWS_SECRET_ACCESS_KEY'))
ASSOCIATE_TAG = str(Config.get_conf('ASSOCIATE_TAG'))

# Accepted Address
ALLOWED_DOMAINS = Config.get_conf('ALLOWED_DOMAINS')

