from .base import *
import os

DEBUG = False
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': os.environ.get('DB_NAME', 'purbeurre'),
		'USER': os.environ.get('DB_USER', 'purbeurre'),
		'PASSWORD': os.environ.get('DB_PASSWORD', '<provideMe>'),
		'HOST': os.environ.get('DB_HOST', 'localhost'),
		'PORT': '',
	},
}

