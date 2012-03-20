from google.appengine.ext import db
from google.appengine.api import namespace_manager

from json_property import JsonProperty

class Config(db.Model):
    value = JsonProperty()

    @classmethod
    def get_conf(cls, key_name):
        namespace = namespace_manager.get_namespace()        
        try:
            namespace_manager.set_namespace('-sysconf-')
            return cls.get_by_key_name(key_name).value
        finally:
            namespace_manager.set_namespace(namespace)

