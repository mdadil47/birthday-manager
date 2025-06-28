from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from .models import Customer

@shared_task
def send_birthday_greetings():
    today = timezone.localdate()
    celebrants = Customer.objects.filter(dob__month=today.month, dob__day=today.day)
    for cust in celebrants:
        if cust.email:
            send_mail(
                subject=f"🎉 Happy Birthday, {cust.name}!",
                message=(
                    f"Dear {cust.name},\n\n"
                    "Your friends at Bistro Bella wish you the happiest of birthdays!\n"
                    "Enjoy a 20% discount the next time you dine with us.\n\n"
                    "Valid for 14 days.\n"
                    "- The Bistro Bella Team"
                ),
                from_email="hello@bistrobella.com",
                recipient_list=[cust.email],
                fail_silently=True,
            )
