import os

POSTMARK_API_KEY = ''

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = ''
AWS_IS_GZIPPED = False
AWS_S3_SECURE_URLS = False

IE_API = InfluenceExplorer('')

AWS_S3_CUSTOM_DOMAIN = "localhost:8000/static"

GIGYA_ENDPOINT = 'https://socialize-api.gigya.com/socialize.shortenURL'
GIGYA_API_KEY = ''
GIGYA_SECRET = ''

DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'adhawk',                      # Or path to database file if using sqlite3.
        'USER': 'blannon',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
            },
        }

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 15

LOG_ROOT = os.path.join(
        os.path.join(os.path.dirname(__file__),os.path.pardir),'logs')

MEDIA_ROOT = os.path.join(
        os.path.join(os.path.dirname(__file__),os.path.pardir),'media')

EXTERNAL_URL = 'http://localhost:8000'
    
yt_developer_key = ''
yt_email = ''
yt_password = ''
