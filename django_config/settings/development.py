from .base import *

# Enable debugging for development
DEBUG = True

# Allow all hosts during development
ALLOWED_HOSTS = ["*"]

# Optionally, add Django Debug Toolbar for local development
INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

# Internal IPs for Debug Toolbar
INTERNAL_IPS = ["127.0.0.1"]

# Lower logging level for more verbose output in development
LOGGING["root"]["level"] = "DEBUG"
