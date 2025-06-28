# BirthdayManager

A Django 5.x web application that helps restaurants track upcoming customer birthdays and automatically send greeting emails.

## Features

* CRUD customer records (name, DOB, contact info, favorite dish)
* Dashboard showing birthdays in the next 30 days
* Daily Celery task to send birthday emails at 09:00 (Asia/Kolkata)
* Django admin for data entry
* SQLite by default; switch to PostgreSQL by editing `settings.py`
* Minimal Tailwind‑style CSS


