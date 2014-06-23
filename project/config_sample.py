# coding: utf-8

# project info
PROJECT_ABBR = 'project'
PROJECT_PATH = "/var/www/%s" % PROJECT_ABBR

# site info
SITE_TITLE = "Project"
SITE_DOMAIN = "http://localhost:5000"
IMAGE_SERVER_URL = "http://localhost"

# app config
DEBUG = True
SECRET_KEY = "\xb5\xb3}#\xb7A\xcac\x9d0\xb6\x0f\x80z\x97\x00\x1e\xc0\xb8+\xe9)\xf0}"
PERMANENT_SESSION_LIFETIME = 3600 * 24 * 7
SESSION_COOKIE_NAME = '%s_session' % PROJECT_ABBR

# image upload path
UPLOADS_DEFAULT_DEST = "/var/www/%s_uploads" % PROJECT_ABBR
UPLOADS_DEFAULT_URL = "%s/%s_uploads/" % (IMAGE_SERVER_URL, PROJECT_ABBR)

# db config
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = ""
SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s/%s" % (DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

# smtp config
mail_host = ""
mail_port = 25
mail_user = ""
mail_pass = ""

# sentry url
SENTRY_DSN = ""

# debug toolbar
DEBUG_TB_INTERCEPT_REDIRECTS = False

# use by fabric
HOST_STRING = ""
