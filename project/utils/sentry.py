from raven.contrib.flask import Sentry
from .. import config

sentry = Sentry(dsn=config.SENTRY_DSN)
