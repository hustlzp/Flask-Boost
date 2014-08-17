# coding: utf-8
from .default import Config


class DevelopmentConfig(Config):
    # App config
    DEBUG = True

    # Uploadsets config
    UPLOADS_DEFAULT_DEST = "/path/to/uploads/resources"  # 上传文件存储路径
    UPLOADS_DEFAULT_URL = "/url/to/uploads/resources"  # 上传文件访问URL

    # SQLAlchemy config
    # 如果是空密码，则直接将password删除即可
    SQLALCHEMY_DATABASE_URI = "mysql://root:password@localhost/proj"
