# coding: utf-8
from .default import Config


class DevelopmentConfig(Config):
    # App config
    DEBUG = True

    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = "mysql://root:password@localhost/#{project}"
