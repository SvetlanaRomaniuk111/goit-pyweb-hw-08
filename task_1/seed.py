import json
import pathlib
import configparser
from mongoengine import connect, errors
from models import Author, Quote

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

if __name__ == '__main__':
    with open('authors.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            try:
                author = Author(fullname=el.get('fullname'),
                                born_date=el.get('born_date'),
                                born_location=el.get('born_location'),
                                description=el.get('description'))
                author.save()
            except errors.NotUniqueError:
                print(f'Author {el.get("fullname")} already exists')

    with open('quotes.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            author = Author.objects(fullname=el.get('author')).first()
            quote = Quote(quote=el.get('quote'), tags=el.get('tags'),
                          author=author)
            quote.save()
