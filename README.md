# BirthdayManager

A Django 5.x web application that helps restaurants track upcoming customer birthdays and automatically send greeting emails.

## Features

* CRUD customer records (name, DOB, contact info, favorite dish)
* Dashboard showing birthdays in the next 30 days
* Daily Celery task to send birthday emails at 09:00 (Asia/Kolkata)
* Django admin for data entry
* SQLite by default; switch to PostgreSQL by editing `settings.py`
* Minimal Tailwind‑style CSS

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open <http://127.0.0.1:8000> in your browser.

### Background tasks

```bash
# worker
celery -A birthday_manager worker -l INFO
# scheduler
celery -A birthday_manager beat -l INFO
```

## Deploy

Set a strong `SECRET_KEY`, configure `DATABASES`, and point `EMAIL_BACKEND` to SendGrid/SES.  
Run Gunicorn behind Nginx and a production‑grade Redis/RabbitMQ broker.
