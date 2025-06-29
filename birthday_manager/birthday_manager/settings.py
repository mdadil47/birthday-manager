"""
Django settings for Birthday‑Manager project.
Works out‑of‑the‑box on Railway and local dev.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# ──────────────────────────────────────────────
# 0. Load .env if present (local dev)
# ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# ──────────────────────────────────────────────
# 1. Core settings
# ──────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY", "dev‑insecure‑key‑change‑me")

DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Railway provides your default domain; add custom ones separated by commas.
ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "127.0.0.1,localhost,birthday-manager-production.up.railway.app"
).split(",")

# ──────────────────────────────────────────────
# 2. Installed apps & middleware
# ──────────────────────────────────────────────
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

# ──────────────────────────────────────────────
# 3. Database – defaults to SQLite, switches to Postgres on Railway
# ──────────────────────────────────────────────
if os.getenv("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600, ssl_require=True
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ──────────────────────────────────────────────
# 4. Password validation
# ──────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ──────────────────────────────────────────────
# 5. Internationalization
# ──────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ──────────────────────────────────────────────
# 6. Static & media files
# ──────────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"        # Gunicorn serves this
STATICFILES_DIRS = [BASE_DIR / "static"]      # your app-level static

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ──────────────────────────────────────────────
# 7. Default primary key type
# ──────────────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ──────────────────────────────────────────────
# 8. Login / logout redirects
# ──────────────────────────────────────────────
LOGIN_REDIRECT_URL = "upcoming_birthdays"
LOGOUT_REDIRECT_URL = "login"

# ──────────────────────────────────────────────
# 9. Security tweaks for production
# ──────────────────────────────────────────────
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
