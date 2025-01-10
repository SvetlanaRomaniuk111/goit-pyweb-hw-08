from typing import List, Any
import pathlib
import configparser
import redis
from redis_lru import RedisLRU
from models import Author, Quote

# Читання конфігураційного файлу
file_config = pathlib.Path(__file__).parent.parent.joinpath(
    'config.ini')
config = configparser.ConfigParser()
config.read(file_config)

user = config.get('DEV_DB', 'USER')
password = config.get('DEV_DB', 'PASSWORD')
domain = config.get('DEV_DB', 'DOMAIN')
db = config.get('DEV_DB', 'DB_NAME')

URI = f"mongodb+srv://{user}:{password}@{domain}/{db}?retryWrites=true&w=majority"

# Підключення до Redis (локальний сервер)
client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str]:
    quotes = Quote.objects(tags__iregex=tag)
    result = set(q.quote for q in quotes)
    return list(result)


@cache
def find_by_tags(tags: List[str]) -> list[str]:
    quotes = Quote.objects(tags__in=tags)
    result = set(q.quote for q in quotes)
    return list(result)


@cache
def find_by_author(author: str) -> list[str]:
    authors = Author.objects(fullname__iregex=f".*{author}.*")
    result = set()
    for a in authors:
        quotes = Quote.objects(author=a)
        result.update(q.quote for q in quotes)
    return list(result)


if __name__ == '__main__':
    while True:
        command = input(
            "Введіть команду (name: Author | tag: tag | tags: tag1,tag2 | exit): ").strip()
        if command.lower() == 'exit':
            break
        try:
            cmd, value = command.split(':')
            cmd = cmd.strip().lower()
            value = value.strip()

            if cmd == 'name':
                quotes = find_by_author(value)
            elif cmd == 'tag':
                quotes = find_by_tag(value)
            elif cmd == 'tags':
                tags = value.split(',')
                quotes = find_by_tags(tags)
            else:
                print("Невідома команда.")
                continue

            for quote in quotes:
                print(quote.encode('utf-8').decode('utf-8'))

        except ValueError:
            print("Невірний формат команди.")
