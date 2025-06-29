"""
Django settings for Birthday‑Manager project
– works in local dev and on Railway.

Key features
============
• DEBUG defaults to True locally, False via env
• SECRET_KEY and other secrets pulled from env
• PostgreSQL auto‑detected with DATABASE_URL
• Static files served by WhiteNoise in production
• ALLOWED_HOSTS & CSRF_TRUSTED_ORIGINS read from env,
  fall back to Railway default domain
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# ────────────────────────────────────────────
# 0. Load .env for local development
# ────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# ────────────────────────────────────────────
# 1. Core settings
# ────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY", "dev‑insecure‑change‑me")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

RAILWAY_DOMAIN = "birthday-manager-production.up.railway.app"
ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    f"127.0.0.1,localhost,{RAILWAY_DOMAIN}"
).split(",")

CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    f"https://{RAILWAY_DOMAIN}"
).split(",")

# ────────────────────────────────────────────
# 2. Applications & middleware
# ────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # local app
    "customers",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise must come right after SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
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

# ────────────────────────────────────────────
# 3. Database: SQLite in dev, Postgres in prod
# ────────────────────────────────────────────
if os.getenv("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            ssl_require=not DEBUG,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ────────────────────────────────────────────
# 4. Password validation
# ────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ────────────────────────────────────────────
# 5. Time & language
# ────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ────────────────────────────────────────────
# 6. Static & media files
# ────────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]  # optional app-level static

# Serve compressed & versioned static files via WhiteNoise
STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ────────────────────────────────────────────
# 7. Auto‑primary‑key
# ────────────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ────────────────────────────────────────────
# 8. Auth redirects
# ────────────────────────────────────────────
LOGIN_REDIRECT_URL = "upcoming_birthdays"
LOGOUT_REDIRECT_URL = "login"

# ────────────────────────────────────────────
# 9. Security for production
# ────────────────────────────────────────────
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
