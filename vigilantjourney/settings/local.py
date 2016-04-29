# vigilantjourney/settings/local.py

from .base import *     # noqa
# import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rg1hqqj(nxq9b5@fmjp-e%(e_@ksma8bhmpe+z^cw^64n=zi#i'

###
CHANNEL_ID = '1234567890'
CHANNEL_SECRET = 'secret'
CHANNEL_MID = '0123456789'
###

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(BASE_DIR), 'db.sqlite3'),
    }
}
