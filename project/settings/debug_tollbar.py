from .installed_apps import INSTALLED_APPS
from .middlewares import MIDDLEWARE


INSTALLED_APPS += ['debug_toolbar',]

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware",] + MIDDLEWARE

# django debug toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]