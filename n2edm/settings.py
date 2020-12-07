import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        # Database driver
        'ENGINE': 'django.db.backends.sqlite3',
        # Replace below with Database Name if using other database engines
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

INSTALLED_APPS = (
    'n2edm.watcher',
    'n2edm.scheduler',
    'n2edm.core',
    'n2edm.models',
    'n2edm.abstract'
)

# SECURITY WARNING: Modify this secret key if using in production!
SECRET_KEY = '6few3nci_q_o@l1dlbk81%wcxe!*6r29yu629&d97!hiqat9fa'
