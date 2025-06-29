from dotenv import load_dotenv
load_dotenv()

import os
from pathlib import Path
import dj_database_url  # Required for Railway DATABASE_URL

BASE_DIR = Path(__file__).resolve().parent.parent

# Load secret key from environment or use a fallback (unsafe for prod)
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-dev-key")

# Debug mode
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Properly parse ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS from env
hosts_env = os.getenv("ALLOWED_HOSTS", "localhost 127.0.0.1")
ALLOWED_HOSTS = ["birthday-manager-production.up.railway.app"]

CSRF_TRUSTED_ORIGINS = [
    f"https://{h}" for h in ALLOWED_HOSTS if not h.startswith(("localhost", "127."))
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",  # Whitenoise app
    "customers",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Whitenoise middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "birthday_manager.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "birthday_manager.wsgi.application"

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=False
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ✅ Static file setup for Railway + Whitenoise
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email (use console backend for testing)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Auth redirects
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "upcoming_birthdays"

# Celery
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")

from celery.schedules import crontab
CELERY_BEAT_SCHEDULE = {
    "send-birthday-greetings": {
        "task": "customers.tasks.send_birthday_greetings",
        "schedule": crontab(hour=9, minute=0),
    },
}
