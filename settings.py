import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# example) SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../3162_SNA_G17/db.sqlite3'),
    }
}
INSTALLED_APPS = (
    'data',
    'django_extensions'

)

SECRET_KEY = '19mdjujzlo2kmooqomsuziu3209idmionduinakaoinsmx'
