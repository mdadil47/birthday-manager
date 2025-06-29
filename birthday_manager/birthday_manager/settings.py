from dotenv import load_dotenv
load_dotenv()
import os
from pathlib import Path
+ import dj_database_url                       # ← NEW (for Railway DB URL parsing)

BASE_DIR = Path(__file__).resolve().parent.parent

- SECRET_KEY = "django-insecure-CHANGE-ME"
- DEBUG = True
- ALLOWED_HOSTS = ["*"]
+ # ------------------------------------------------------------------
+ # Core security & env settings (use Railway dashboard to set the vars)
+ # ------------------------------------------------------------------
+ SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-dev-key")        # ← NEW
+ DEBUG = os.getenv("DEBUG", "False").lower() == "true"                # ← NEW
+
+ # Railway sets the domain after the first deploy; add it in the UI,
+ # e.g. birthday-manager-production.up.railway.app
+ ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost 127.0.0.1").split()
+
+ # Add the same hosts *with* scheme for Django’s CSRF checker
+ CSRF_TRUSTED_ORIGINS = [
+     f"https://{host}" for host in ALLOWED_HOSTS
+     if not host.startswith(("localhost", "127."))
+ ]                                                                    # ← NEW

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
+   "whitenoise.runserver_nostatic",   # ← NEW (serves static files in prod)
    "customers",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
+   "whitenoise.middleware.WhiteNoiseMiddleware",  # ← NEW
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ------------------------------------------------------------------
# Database: use Railway’s DATABASE_URL if present
# ------------------------------------------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=False,  # set True if Railway DB requires SSL
    )
}

# ------------------------------------------------------------------
# Static files (CSS, JS, images) – required for Railway
# ------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"            # ← NEW
STATICFILES_DIRS = [BASE_DIR / "static"]          # already present
STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)                                                 # ← NEW

# ------------------------------------------------------------------
# Everything below this line stays unchanged …
# ------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
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
