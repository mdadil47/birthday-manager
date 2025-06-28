from datetime import date
from django.db import models

class Customer(models.Model):
    name         = models.CharField(max_length=255)
    dob          = models.DateField("Date of birth")
    email        = models.EmailField(blank=True, null=True)
    phone        = models.CharField(max_length=20, blank=True, null=True)
    last_visit   = models.DateField(blank=True, null=True)

    # ✅ replace favorite_dish with last_billing
    last_billing = models.DecimalField(
        "Last billing amount (₹)",
        max_digits=10, decimal_places=2,
        blank=True, null=True
    )

    def __str__(self):
        return self.name

    @property
    def next_birthday(self):
        today = date.today()
        this_year = self.dob.replace(year=today.year)
        return this_year if this_year >= today else this_year.replace(year=today.year + 1)
