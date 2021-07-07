import os
# from settings.env import env
from starlette.templating import Jinja2Templates

ROOT = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_URL = '/static/'
STATICFILES_ROOT = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TEMPLATES = Jinja2Templates(directory="templates")

# email settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'testrpharm@gmail.com'
EMAIL_HOST_PASSWORD = 'rpharmdb'
EMAIL_PORT = 587