# ─────────────────────────
# 1. Base image
# ─────────────────────────
FROM python:3.11-slim

# Install system libs for psycopg2 / Pillow if needed
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# ─────────────────────────
# 2. Environment
# ─────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# ─────────────────────────
# 3. Install deps
# ─────────────────────────
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ─────────────────────────
# 4. Copy project code
# ─────────────────────────
COPY . .

# ─────────────────────────
# 5. Start script
# ─────────────────────────
# Runs migrations, collects static, then starts Gunicorn
CMD ["sh", "-c", \
    "python manage.py migrate --noinput && \
     python manage.py collectstatic --noinput && \
     gunicorn birthday_manager.wsgi:application --bind 0.0.0.0:8000"]
