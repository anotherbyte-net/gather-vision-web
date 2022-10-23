"""
Django settings for gather-vision project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import importlib.resources
import pathlib

from gather_vision_web.proj.settings_env import SettingsEnv

# Use django-environ to load settings.
env = SettingsEnv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
with importlib.resources.path("gather_vision_web.proj", "settings") as p:
    BASE_DIR = pathlib.Path(p).resolve().parent.parent

# Load the settings from the env file.
# Check the DJANGO_ENV_FILE env var first, then default to local .env file.
env.read_env(env.str("DJANGO_ENV_FILE", str(BASE_DIR.parent.parent / ".local" / ".env")))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", str, [])
INTERNAL_IPS = env.list("INTERNAL_IPS", str, ["127.0.0.1"])

# Installed applications
# https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-INSTALLED_APPS
INSTALLED_APPS = [
    "django.contrib.admindocs",
    "django.contrib.admin.apps.SimpleAdminConfig",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "gather_vision_web.apps.explore.apps.ExploreAppConfig",
    "gather_vision_web.apps.electricity.apps.ElectricityAppConfig",
    "gather_vision_web.apps.legislatures.apps.LegislaturesAppConfig",
    "gather_vision_web.apps.music.apps.MusicAppConfig",
    "gather_vision_web.apps.transport.apps.TransportAppConfig",
    "gather_vision_web.apps.water.apps.WaterAppConfig",
]

if DEBUG is True:
    INSTALLED_APPS.append("debug_toolbar")

# Middleware: Django 'plugins' to alter input and output
# https://docs.djangoproject.com/en/4.0/topics/http/middleware/
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Root URL conf: import path for the project-level url conf.
# https://docs.djangoproject.com/en/4.0/ref/settings/#root-urlconf
ROOT_URLCONF = "gather_vision_web.proj.urls"

# Django template engines.
# https://docs.djangoproject.com/en/4.0/ref/settings/#templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI app for the Django dev server.
# https://docs.djangoproject.com/en/4.0/ref/settings/#wsgi-application
WSGI_APPLICATION = "gather_vision_web.proj.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {"default": env.db_url()}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGE_CODE = "en-au"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Cache
# https://docs.djangoproject.com/en/4.0/topics/cache
CACHES = {"default": env.cache_url()}

# Fixtures
# https://docs.djangoproject.com/en/4.0/howto/initial-data
# FIXTURE_DIRS = [str(pathlib.Path(i).as_posix()) for i in [env.str("DJANGO_FIXTURES_DIR")] if i]

# Custom user model
# https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
AUTH_USER_MODEL = "explore.CustomUser"

# logging
# https://docs.djangoproject.com/en/4.0/topics/logging
LOGGING_LEVEL = env.str("DJANGO_LOG_LEVEL", "DEBUG")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "{asctime} [{levelname:8} {name}] - {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "level": LOGGING_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOGGING_LEVEL,
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "propagate": True,
        },
    },
}
