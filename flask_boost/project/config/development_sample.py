# coding: utf-8
from .default import Config


class DevelopmentConfig(Config):
    # App config
    DEBUG = True

    # SQLAlchemy config
    # 如果是空密码，则直接将password删除即可
    SQLALCHEMY_DATABASE_URI = "mysql://root:password@localhost/#{project}"
