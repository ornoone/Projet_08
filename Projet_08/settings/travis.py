from .base import *

DATABASES = {
    'default': {
	 'ENGINE': 'django.db.backends.postgresql',
	 'NAME': 'postgres',
	 'USER': 'postgres',
	 'PASSWORD': '',
	 'HOST': '',
	 'PORT': '',
         'OPTIONS': {
            'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
        },
    },
}

