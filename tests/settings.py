import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append("%s/.." % TEST_DIR)

COMPRESS_CACHE_BACKEND = 'locmem://'

DATABASE_ENGINE = 'sqlite3'

INSTALLED_APPS = (
    'django_coverage',
    'urlmiddleware',
    'test_urlmiddleware',
)

TEMPLATE_DIRS = (
)

MIDDLEWARE_CLASSES = (
    'urlmiddleware.URLMiddleware',
)

ROOT_URLCONF = 'test_urlmiddleware.urls'

COVERAGE_ADDITIONAL_MODULES = ['urlmiddleware', ]
