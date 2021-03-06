import os
from urllib.parse import urlparse

from django.conf import settings as s


def strip_password(url):
    parsed = urlparse(url)
    replaced = parsed._replace(
        netloc="{}@{}".format(parsed.username, parsed.hostname))
    return replaced.geturl()


def settings(request):
    if s.RAVEN_CONFIG.get('dsn'):
        raven_dsn = strip_password(s.RAVEN_CONFIG['dsn'])
    else:
        raven_dsn = ''

    return dict(
        settings=dict(
            INSTANCE=os.getenv('INSTANCE'),
            SENTRY_DSN=raven_dsn,
        )
    )
