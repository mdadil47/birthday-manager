# ---- Base image ----
FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# ---- Install dependencies ----
# (Copy requirements first to leverage Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy project ----
COPY . .

# ---- Collect static and run migrations at build time ----
#   • If you prefer to migrate at runtime, delete the migrate line here
#   • Ensure 'DEBUG=False' and Whitenoise/static settings are already in settings.py
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --noinput

# ---- Gunicorn entrypoint ----
# Render sets $PORT automatically; most other hosts do the same.
CMD ["gunicorn", "birthday_manager.wsgi:application", "--bind", "0.0.0.0:${PORT:-8080}"]
