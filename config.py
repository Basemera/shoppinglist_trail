import os
basedir = os.path.abspath(os.path.dirname(__file__))
# config.py
WTF_CSRF_ENABLED = True


# Enable Flask's debugging features. Should be False in production
DEBUG = True
SECRET_KEY = 'im-actually-quite-aweome:)'