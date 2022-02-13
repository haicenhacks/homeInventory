import os


class Database:
    NAME = os.getenv('POSTGRES_DB')
    USER = os.getenv('POSTGRES_USER')
    PASSWORD = os.getenv('POSTGRES_PASSWORD')
    HOST = os.getenv('DATABASE_HOST')
    PORT = os.getenv('DATABASE_PORT')


class Secrets:
    if not os.getenv('DOCKER'):
        SECRET_KEY = "JlJCzokOhn41JrQEaWGwX7pkvBpSC8JcZ-uZar97prg"
    else:
        SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
