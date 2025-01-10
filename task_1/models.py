import pathlib
import configparser
from mongoengine import connect, Document, StringField, ReferenceField, \
    ListField, CASCADE

# Читання конфігураційного файлу
file_config = pathlib.Path(__file__).parent.parent.joinpath(
    'config.ini')  # ../config.ini
config = configparser.ConfigParser()
config.read(file_config)

user = config.get('DEV_DB', 'USER')
password = config.get('DEV_DB', 'PASSWORD')
domain = config.get('DEV_DB', 'DOMAIN')
db = config.get('DEV_DB', 'DB_NAME')

URI = f"mongodb+srv://{user}:{password}@{domain}/{db}?retryWrites=true&w=majority"

# Підключення до хмарної бази даних MongoDB
connect(host=URI)

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=15))
    quote = StringField()
    meta = {"collection": "quotes"}

    def to_json(self):
        return {
            "author": self.author.fullname,
            "tags": self.tags,
            "quote": self.quote
        }