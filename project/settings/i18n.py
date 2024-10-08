# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
from . import BASE_DIR

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locale'
]
