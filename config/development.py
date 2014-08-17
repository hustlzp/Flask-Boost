# coding: utf-8
from .default import Config


class DevelopmentConfig(Config):
    # App config
    DEBUG = True

    # Uploadsets config
    UPLOADS_DEFAULT_DEST = "/Library/WebServer/Documents/proj_uploads"
    UPLOADS_DEFAULT_URL = "http://localhost/proj_uploads/"

    # Db config
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/proj"
