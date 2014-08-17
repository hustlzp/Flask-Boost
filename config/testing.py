# coding: utf-8
from .default import Config


class TestingConfig(Config):
    # App config
    TESTING = True

    # Disable csrf while testing
    WTF_CSRF_ENABLED = False

    # Uploadsets config
    UPLOADS_DEFAULT_DEST = ""
    UPLOADS_DEFAULT_URL = ""

    # Db config
    SQLALCHEMY_DATABASE_URI = "sqlite:///%s/db/testing.sqlite3" % Config.PROJECT_PATH

